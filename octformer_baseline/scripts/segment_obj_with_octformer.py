#!/usr/bin/env python3
"""
Segment an .obj mesh with OctFormer.

- Loads a mesh (.obj) with trimesh
- Uniformly samples N surface points
- Builds OctFormer from a config + checkpoint
- Runs semantic segmentation on the sampled points
- Propagates per-point labels back to mesh vertices (nearest neighbor)
- Writes colored .ply and .obj (with .mtl), plus a .npz with arrays

Usage:
  python segment_obj_with_octformer.py \
      --obj path/to/mesh.obj \
      --checkpoint path/to/scannet_checkpoint.pth \
      --config octformer/configs/seg_scannet.yaml \
      --out out/mesh_segmented \
      --num-points 200000 \
      --device cuda \
      --octformer-root ./octformer
"""

import argparse
import os
import sys
import json
import numpy as np
import torch

# ---- robust import of octformer modules ----
def add_repo_to_syspath(oct_root):
    oct_root = os.path.abspath(oct_root)
    if oct_root not in sys.path:
        sys.path.insert(0, oct_root)

# ---- mesh / io utils ----
def load_mesh_trimesh(obj_path):
    import trimesh
    mesh = trimesh.load(obj_path, force='mesh')
    if isinstance(mesh, trimesh.Scene):
        # merge scene into a single mesh
        mesh = trimesh.util.concatenate(
            [g for g in mesh.dump() if isinstance(g, trimesh.Trimesh)]
        )
    if mesh.vertices.shape[0] == 0 or mesh.faces.shape[0] == 0:
        raise ValueError("Empty mesh after load.")
    mesh.remove_unreferenced_vertices()
    mesh.remove_degenerate_faces()
    mesh.remove_infinite_values()
    mesh.rezero()  # move near origin
    return mesh

def sample_points_on_surface(mesh, n_pts):
    # returns (P,3) xyz and (P,3) normals if available
    # uses area-weighted uniform sampling
    import trimesh
    pts, face_idx = trimesh.sample.sample_surface_even(mesh, n_pts)
    # vertex normals -> face normals -> point normals (approx using face)
    face_normals = mesh.face_normals
    norms = face_normals[face_idx]
    return pts.astype(np.float32), norms.astype(np.float32)

def normalize_points(points, center=True, scale_to_unit=True):
    pts = points.copy()
    if center:
        ctr = pts.mean(axis=0, keepdims=True)
        pts -= ctr
    if scale_to_unit:
        # scale to fit inside unit sphere
        m = np.linalg.norm(pts, axis=1).max()
        if m > 0:
            pts /= m
    return pts

# ---- color / class helpers (ScanNet20 example) ----
SCANNET20_NAMES = [
    'wall','floor','cabinet','bed','chair','sofa','table','door','window',
    'bookshelf','picture','counter','desk','curtain','refrigerator','shower curtain',
    'toilet','sink','bathtub','other furniture'
]
SCANNET20_COLORS = np.array([
    [174,199,232],[152,223,138],[31,119,180],[255,187,120],[188,189,34],
    [140,86,75],[255,152,150],[214,39,40],[197,176,213],[148,103,189],
    [196,156,148],[23,190,207],[247,182,210],[219,219,141],[255,127,14],
    [227,119,194],[158,218,229],[44,160,44],[112,128,144],[82,84,163]
], dtype=np.uint8)

def colors_for_labels(labels, n_classes=20):
    colors = np.zeros((labels.size, 3), dtype=np.uint8)
    if n_classes == 20:
        palette = SCANNET20_COLORS
    else:
        # simple repeating palette
        rng = np.random.default_rng(0)
        palette = (rng.random((n_classes,3))*255).astype(np.uint8)
    colors[:] = palette[labels % len(palette)]
    return colors

# ---- nearest neighbor (CPU or faiss if available) ----
def knn_labels_to_vertices(verts, pts, pt_labels):
    try:
        import faiss  # optional acceleration
        index = faiss.IndexFlatL2(3)
        index.add(pts.astype(np.float32))
        _, idx = index.search(verts.astype(np.float32), 1)
        vlabels = pt_labels[idx[:,0]]
        return vlabels
    except Exception:
        # numpy fallback
        # chunk to save memory
        vlabels = np.empty((verts.shape[0],), dtype=pt_labels.dtype)
        CH = 50000
        for s in range(0, verts.shape[0], CH):
            e = min(s+CH, verts.shape[0])
            d2 = ((verts[s:e,None,:] - pts[None,:,:])**2).sum(axis=2)
            nn = d2.argmin(axis=1)
            vlabels[s:e] = pt_labels[nn]
        return vlabels

# ---- write outputs ----
def write_ply(path, verts, faces, vcolors=None, vlabels=None):
    # minimal PLY writer (ASCII)
    with open(path, 'w') as f:
        f.write("ply\nformat ascii 1.0\n")
        n_v = len(verts); n_f = len(faces)
        props = ["property float x","property float y","property float z"]
        if vcolors is not None:
            props += ["property uchar red","property uchar green","property uchar blue"]
        if vlabels is not None:
            props += ["property int label"]
        f.write(f"element vertex {n_v}\n")
        for p in props:
            f.write(p+"\n")
        f.write(f"element face {n_f}\n")
        f.write("property list uchar int vertex_indices\nend_header\n")
        for i in range(n_v):
            line = list(map(float, verts[i].tolist()))
            if vcolors is not None:
                line += list(map(int, vcolors[i].tolist()))
            if vlabels is not None:
                line += [int(vlabels[i])]
            f.write(" ".join(map(str,line))+"\n")
        for i in range(n_f):
            a,b,c = faces[i]
            f.write(f"3 {int(a)} {int(b)} {int(c)}\n")

def write_obj_with_mtl(base_out, verts, faces, colors):
    # write OBJ + MTL with per-vertex colors baked via per-class materials
    obj_path = base_out + ".obj"
    mtl_path = base_out + ".mtl"
    # group vertices by color
    unique_cols, inv = np.unique(colors, axis=0, return_inverse=True)
    with open(mtl_path, "w") as mtl:
        for i, col in enumerate(unique_cols):
            r,g,b = (col/255.0).tolist()
            mtl.write(f"newmtl m{i}\nKd {r:.4f} {g:.4f} {b:.4f}\nKa 0 0 0\nKs 0 0 0\nd 1\nillum 1\n\n")
    with open(obj_path, "w") as obj:
        obj.write(f"mtllib {os.path.basename(mtl_path)}\n")
        for v in verts:
            obj.write(f"v {v[0]} {v[1]} {v[2]}\n")
        # write faces grouped by material
        for m_id in range(unique_cols.shape[0]):
            obj.write(f"usemtl m{m_id}\n")
            mask = (inv == m_id)
            # faces whose all three verts have this material
            # (simple choice to keep viewers happy)
            # More advanced: split faces by majority label.
            # Here, we'll handle majority label:
            # build face labels by majority of its 3 vertices
        # majority label per face
        # compute once:
        # map each vertex to class id by its color index (inv)
        vmat = inv
        # majority per face:
        f_mats = []
        for a,b,c in faces:
            xs = [vmat[a], vmat[b], vmat[c]]
            maj = xs[0] if (xs.count(xs[0])>=2) else (xs[1] if xs[1]==xs[2] else xs[2])
            f_mats.append(maj)
        f_mats = np.array(f_mats, dtype=np.int32)
        for m_id in range(unique_cols.shape[0]):
            obj.write(f"usemtl m{m_id}\n")
            idx = np.where(f_mats==m_id)[0]
            for i in idx:
                a,b,c = faces[i]
                obj.write(f"f {a+1} {b+1} {c+1}\n")

# ---- build & run octformer ----
def build_octformer(config_path, checkpoint_path, oct_root):
    """
    Build an OctFormer segmentation model using the repo's segmentation builder.
    """
    import yaml
    from yacs.config import CfgNode as CN
    import os, sys
    # ensure we can import from the repository
    oct_root = os.path.abspath(oct_root)
    if oct_root not in sys.path:
        sys.path.insert(0, oct_root)

    from segmentation import build_segmentation_model

    # load YAML into config
    with open(config_path, 'r') as f:
        cfg = CN(yaml.safe_load(f))

    model = build_segmentation_model(cfg)

    import torch
    ckpt = torch.load(checkpoint_path, map_location='cpu')
    state = ckpt.get('state_dict', ckpt.get('model', ckpt))
    missing, unexpected = model.load_state_dict(state, strict=False)
    if missing:
        print("[warn] missing keys:", len(missing))
    if unexpected:
        print("[warn] unexpected keys:", len(unexpected))
    model.eval()
    return model, cfg

@torch.no_grad()
def infer_points(model, cfg, points, device='cuda'):
    # points: (P,3) float32 normalized
    # Many configs expect BxNx3 tensor
    x = torch.from_numpy(points[None, ...])  # (1,P,3)
    x = x.to(device)
    model = model.to(device)
    # Some implementations also expect features (like RGB) or normals.
    # We'll pass only coordinates; if the model needs feats, it should have defaults.
    out = model(x)  # assume returns logits BxPxC or dict
    if isinstance(out, dict):
        if 'logits' in out: logits = out['logits']
        elif 'pred' in out: logits = out['pred']
        else:
            # try the first tensor in dict
            logits = next(v for v in out.values() if torch.is_tensor(v))
    else:
        logits = out
    labels = logits.argmax(dim=-1).squeeze(0).detach().cpu().numpy().astype(np.int32)
    return labels

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obj", required=True, help="Path to .obj mesh")
    ap.add_argument("--checkpoint", required=True, help="Path to OctFormer .pth")
    ap.add_argument("--config", required=True, help="Path to OctFormer YAML config")
    ap.add_argument("--out", required=True, help="Output path without extension")
    ap.add_argument("--num-points", type=int, default=200000)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--octformer-root", default="./octformer")
    ap.add_argument("--no-normalize", action="store_true", help="Skip centering/scaling")
    args = ap.parse_args()

    add_repo_to_syspath(args.octformer_root)
    mesh = load_mesh_trimesh(args.obj)
    pts, norms = sample_points_on_surface(mesh, args.num_points)
    pts_n = pts if args.no_normalize else normalize_points(pts)

    model, cfg = build_octformer(args.config, args.checkpoint)
    labels_p = infer_points(model, cfg, pts_n, device=args.device)

    # map labels to vertices
    verts = np.asarray(mesh.vertices, dtype=np.float32)
    faces = np.asarray(mesh.faces, dtype=np.int32)
    vlabels = knn_labels_to_vertices(verts, pts, labels_p)

    # choose colors from labels
    n_classes = int(labels_p.max())+1
    colors_v = colors_for_labels(vlabels, n_classes=n_classes)

    # write outputs
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    ply_path = args.out + ".ply"
    write_ply(ply_path, verts, faces, colors_v, vlabels)

    # obj+mtl
    write_obj_with_mtl(args.out, verts, faces, colors_v)

    # npz (raw)
    npz_path = args.out + ".npz"
    np.savez_compressed(npz_path,
                        verts=verts, faces=faces,
                        points=pts, points_normed=pts_n,
                        labels_p=labels_p, labels_v=vlabels)

    # metadata json
    meta = {
        "classes": SCANNET20_NAMES if n_classes==20 else list(range(n_classes)),
        "obj": os.path.abspath(args.obj),
        "checkpoint": os.path.abspath(args.checkpoint),
        "config": os.path.abspath(args.config),
        "num_points": args.num_points,
        "normalized": not args.no_normalize
    }
    with open(args.out + ".json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"[ok] wrote:\n  {ply_path}\n  {args.out}.obj/.mtl\n  {npz_path}\n  {args.out}.json")

if __name__ == "__main__":
    main()

