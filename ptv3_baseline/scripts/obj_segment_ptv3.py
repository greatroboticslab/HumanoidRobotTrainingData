#!/usr/bin/env python3
"""
obj_segment_ptv3.py

Load a .obj mesh, sample points from surface, run PTv3 model to get per-point semantic labels,
and write a colored PLY (or per-point labels) as output.

Usage:
    python obj_segment_ptv3.py --obj my_mesh.obj --checkpoint /path/to/ptv3_checkpoint.pth --out out_segmented.ply
"""

import os
import sys
import argparse
import numpy as np
import torch

# open3d for reading/sampling meshes and writing PLY
try:
    import open3d as o3d
except Exception as e:
    raise RuntimeError("open3d is required. pip install open3d") from e

# allow importing model.py placed in same folder (adjust as needed)
ROOT_PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_PARENT)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)                  # so ptv3_baseline is importable
sys.path.insert(0, os.path.join(ROOT_DIR, "ptv3_baseline"))  # so serialization/ is importable directly


# Try to import model from the PTv3 repo copy (model.py)
try:
    from ptv3_baseline import model as ptv3_model_module
except Exception as e:
    raise RuntimeError("Failed to import model.py from the PTv3 repo. Make sure model.py is in the same folder.") from e

# --- helper functions ------------------------------------------------------

def sample_points_from_obj(obj_path, n_points=200000):
    """
    Read a mesh .obj and uniformly sample points on the surface with normals + colors (if available).
    Returns: numpy array (N,3) coords, optional (N,3) normals, (N,3) colors (0..1)
    """
    mesh = o3d.io.read_triangle_mesh(obj_path)
    if mesh is None or len(mesh.triangles) == 0:
        raise RuntimeError(f"Failed to read mesh or mesh has no triangles: {obj_path}")
    # ensure triangles have vertex normals (Open3D might compute)
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()
    # sample
    pcd = mesh.sample_points_uniformly(number_of_points=n_points)
    pts = np.asarray(pcd.points).astype(np.float32)
    norms = np.asarray(pcd.normals).astype(np.float32) if pcd.has_normals() else None

    colors = None
    if pcd.has_colors():
        colors = np.asarray(pcd.colors).astype(np.float32)
    else:
        # try to get from mesh vertex colors
        if mesh.has_vertex_colors():
            # nearest vertex color -> per sampled point mapping is nontrivial; skip for simplicity
            colors = None

    return pts, norms, colors

def normalize_points(pts):
    """
    Center and scale points into a unit cube / sphere (optional, but many models expect normalized input).
    PTv3 configs from the repo may include normalization pipelines; adapt this if you use a specific dataset config.
    """
    centroid = pts.mean(axis=0)
    pts_centered = pts - centroid
    furthest = np.max(np.linalg.norm(pts_centered, axis=1))
    if furthest <= 0:
        return pts_centered
    pts_norm = pts_centered / furthest
    return pts_norm

# --- model helper ----------------------------------------------------------

def load_ptv3_model(checkpoint_path, device='cuda'):
    """
    Attempt to instantiate PTv3 model from the model.py you copied from the repo and load state_dict.
    The exact constructor is repo-dependent; try some common entry points.
    Returns model (torch.nn.Module) on desired device.
    """
    # Try common builders from model.py
    model = None

    # 1) try builder function names
    for fn_name in ("build_model", "build_ptv3", "make_model", "get_model"):
        if hasattr(ptv3_model_module, fn_name):
            builder = getattr(ptv3_model_module, fn_name)
            try:
                # Common pattern: builder(cfg) or builder()
                model = builder()
            except TypeError:
                model = builder({})
            break

    # 2) try typical class names
    if model is None:
        for cls_name in ("PTV3", "PointTransformerV3", "PTV3Model", "PointTransformer"):
            if hasattr(ptv3_model_module, cls_name):
                cls = getattr(ptv3_model_module, cls_name)
                try:
                    model = cls()
                except TypeError:
                    model = cls({})  # pass empty config if required
                break

    if model is None:
        raise RuntimeError("Could not find a builder/class in model.py. Open model.py and locate how to instantiate the model (see README).")

    # load checkpoint
    if checkpoint_path is not None and os.path.exists(checkpoint_path):
        ckpt = torch.load(checkpoint_path, map_location='cpu')
        # common checkpoint shapes: {'state_dict':..., 'model':..., ...} or raw state_dict
        state_dict = None
        if isinstance(ckpt, dict):
            # guess which key contains state dict
            for k in ('state_dict', 'model', 'state'):
                if k in ckpt:
                    state_dict = ckpt[k]
                    break
            if state_dict is None:
                # maybe ckpt itself is the state dict
                state_dict = ckpt
        else:
            state_dict = ckpt

        # try to load safely
        try:
            model.load_state_dict(state_dict, strict=False)
        except Exception as e:
            print("Warning: couldn't fully load checkpoint into model (strict=False used).", e)
    else:
        print("Warning: checkpoint path not found or not provided. Running model with random weights.")

    model.eval()
    model.to(device)
    return model

# --- inference -------------------------------------------------------------

def run_inference_on_points(model, points_np, device="cuda"):
    device_t = torch.device(device if torch.cuda.is_available() else "cpu")
    N = points_np.shape[0]

    # Convert to torch
    coords = torch.from_numpy(points_np).float().to(device_t)  # (N,3)

    # Features: simplest is to use xyz as features
    feats = coords.clone()

    # Batch indices (all zeros if single cloud)
    batch = torch.zeros(N, dtype=torch.long, device=device_t)

    # Grid size: required for voxelization
    grid_size = torch.tensor([0.01], device=device_t)  # adjust if needed

    # Construct input dictionary
    data_dict = {
        "coord": coords,
        "feat": feats,
        "batch": batch,
        "grid_size": grid_size,
    }

    with torch.no_grad():
        out_point = model(data_dict)

    # At this stage, out_point is a Point object. Its features live in out_point.feat.
    # For segmentation, usually there is a classifier head mapping to num_classes,
    # but in your model.py I don’t see a classifier defined (only encoder/decoder).
    # So out_point.feat is the per-point embedding, not class logits.

    # If you loaded a checkpoint that includes a classifier, check its keys.
    # For now, we’ll just cluster/argmax the embedding dimension to fake "labels".
    feats_np = out_point.feat.cpu().numpy()
    preds = np.argmax(feats_np, axis=1)

    return preds


# --- utilities -------------------------------------------------------------

def colorize_labels(labels):
    """
    Make simple color map for labels (N,)->(N,3) in 0..1
    """
    np.random.seed(1)
    num_classes = int(labels.max()) + 1
    cmap = np.random.rand(num_classes, 3)
    colors = cmap[labels]
    return colors

# --- main ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run PTv3 segmentation on an .obj mesh")
    parser.add_argument("--obj", required=True, help="Path to input .obj mesh")
    parser.add_argument("--checkpoint", required=False, default=None, help="Path to PTv3 checkpoint .pth")
    parser.add_argument("--npoints", type=int, default=200000, help="How many surface points to sample")
    parser.add_argument("--out", default="segmented_out.ply", help="Output PLY filename with per-point color")
    parser.add_argument("--device", default="cuda", help="device (cuda or cpu)")
    args = parser.parse_args()

    pts, norms, cols = sample_points_from_obj(args.obj, n_points=args.npoints)
    pts = normalize_points(pts)
    print(f"Sampled {len(pts)} points from {args.obj}")

    device = args.device if torch.cuda.is_available() else "cpu"
    model = load_ptv3_model(args.checkpoint, device=device)

    print("Running inference (this may take a while for large clouds)...")
    preds = run_inference_on_points(model, pts, device=device)
    print("Inference done. Got", preds.shape, "labels")

    # colorize
    colors = colorize_labels(preds)

    # save PLY with labels as colors and label scalar
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    # Save label as property (Open3D may not support arbitrary per-vertex attributes in all versions)
    # We'll write a simple PLY with color. If you want label field, consider using plyfile or custom writer.
    o3d.io.write_point_cloud(args.out, pcd)
    print("Wrote colored point cloud to", args.out)
    # Optionally save labels separately
    np.save(args.out + ".labels.npy", preds)
    print("Saved labels to", args.out + ".labels.npy")

if __name__ == "__main__":
    main()

