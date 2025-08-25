import open3d as o3d
import numpy as np
import sys
sys.path.append("../")
import torch
from vggt.models.vggt import VGGT
from vggt.utils.load_fn import load_and_preprocess_images
from visual_util import predictions_to_glb

def world_points_to_obj(world_points, filename="output.obj", sample_stride=1):
    """
    Convert VGGT world_points tensor to an OBJ point cloud.

    Args:
        world_points: torch.Tensor of shape [B, V, H, W, 3] or [B, H, W, 3]
        filename: path to save .obj
        sample_stride: take every Nth pixel to reduce density (default 1 = all points)
    """
    # Remove batch/view dims if present
    pts = world_points.squeeze().detach().cpu()  # shape [H, W, 3] or [V, H, W, 3]

    # If view dim exists, collapse it
    if pts.dim() == 4:  # [V, H, W, 3]
        pts = pts.reshape(-1, pts.shape[-2], pts.shape[-1], 3)[0]  # pick first view

    # Flatten HxW → N
    pts = pts.reshape(-1, 3)

    # Optionally downsample (useful if image is huge)
    if sample_stride > 1:
        pts = pts[::sample_stride]

    # Write to .obj
    with open(filename, "w") as f:
        for p in pts:
            f.write(f"v {p[0].item()} {p[1].item()} {p[2].item()}\n")

    print(f"Saved {pts.shape[0]} points to {filename}")



def pointcloud_to_mesh(world_points, obj_filename="mesh.obj", img=None):
    """
    Convert VGGT world_points tensor to a surface mesh (.obj).
    Optionally assign UVs from image coords.

    Args:
        world_points: torch.Tensor [B, H, W, 3]
        obj_filename: path to save mesh
        img: optional HxW(,3) numpy array with image colors for texture
    """
    # Flatten world points
    pts = world_points.squeeze().detach().cpu().numpy()  # [H, W, 3]
    H, W, _ = pts.shape
    pts_flat = pts.reshape(-1, 3)

    # Make Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts_flat)

    if img is not None:
        colors = img.reshape(-1, 3) / 255.0
        pcd.colors = o3d.utility.Vector3dVector(colors)

    # Estimate normals (needed for meshing)
    pcd.estimate_normals()

    # Run Poisson reconstruction
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
    mesh = mesh.remove_degenerate_triangles()
    mesh = mesh.remove_duplicated_triangles()
    mesh = mesh.remove_non_manifold_edges()
    mesh = mesh.remove_unreferenced_vertices()

    # Save
    o3d.io.write_triangle_mesh(obj_filename, mesh)
    print(f"Saved mesh to {obj_filename}")
    return mesh


def ball_pivot_mesh(world_points, obj_filename="mesh.obj", radius=0.01):

    pts = world_points.squeeze().detach().cpu().numpy()
    pts = pts.reshape(-1, 3)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    pcd.estimate_normals()

    # Radii for ball pivot (try a few multiples of average spacing)
    radii = [radius, radius * 2, radius * 4]
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii)
    )

    o3d.io.write_triangle_mesh(obj_filename, mesh)
    print(f"Saved Ball Pivoting mesh to {obj_filename}")
    return mesh

device = "cuda" if torch.cuda.is_available() else "cpu"
# bfloat16 is supported on Ampere GPUs (Compute Capability 8.0+) 
dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16

# Initialize the model and load the pretrained weights.
# This will automatically download the model weights the first time it's run, which may take a while.
model = VGGT.from_pretrained("facebook/VGGT-1B").to(device)

# Load and preprocess example images (replace with your own image paths)
image_names = ["tomato.jpg"]
images = load_and_preprocess_images(image_names).to(device)


with torch.no_grad():
    with torch.cuda.amp.autocast(dtype=dtype):
        # Predict attributes including cameras, depth maps, and point maps.
        predictions = model(images)
        #print(predictions)
        print(predictions.keys())
        print(predictions["world_points"])

        
        world_points = predictions["world_points"]
        world_points_to_obj(world_points)
#        ball_pivot_mesh(world_points, "tomato.obj")
