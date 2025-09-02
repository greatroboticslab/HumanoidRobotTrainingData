import os
import open3d as o3d
import numpy as np
import sys
sys.path.append("../")
import torch
from vggt.models.vggt import VGGT
from vggt.utils.load_fn import load_and_preprocess_images
from visual_util import predictions_to_glb
import pymeshlab

import argparse

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--downsample', type=int, default=1, help='Downsample the mesh/pointcloud by this much. Higher value = less verticies. Reccommended value for games/simulations = 96.')
parser.add_argument('--input', type=str, default='', help='Image file to convert to a 3D pointcloud.')
parser.add_argument('--dir', type=str, default='', help='Folder to process. All images in this folder will be turned into meshes.')
parser.add_argument('--start', type=int, default=0, help='Start from this file #')
parser.add_argument('--end', type=int, default=-1, help='Stop processing at this file, set to -1 for all files from start.')

args = parser.parse_args()


def world_points_to_obj(world_points, filename="output.obj", foldername="", sample_stride=1):
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

    os.makedirs("../output/"+foldername + "/", exist_ok=True)

    # Write to .obj
    with open("../output/" + foldername + "/" + filename + ".obj", "w") as f:
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


def ball_pivot_mesh(obj_filename, radius=0.01):

    print(obj_filename)

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(obj_filename)

device = "cuda" if torch.cuda.is_available() else "cpu"
# bfloat16 is supported on Ampere GPUs (Compute Capability 8.0+) 
dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16

# Initialize the model and load the pretrained weights.
# This will automatically download the model weights the first time it's run, which may take a while.
model = VGGT.from_pretrained("facebook/VGGT-1B").to(device)

if args.input == "":

    #Do loop

    frameDir = args.dir

    onlyFolders = [name for name in os.listdir(frameDir) if os.path.isfile(os.path.join(frameDir, name))]


    _from = args.start
    if _from > len(onlyFolders):
        _from = len(onlyFolders)
    _to = args.end
    if _to > len(onlyFolders):
        _to = len(onlyFolders)
    onlyFolders = onlyFolders[_from:_to]

    for file in onlyFolders:
        image_names = [args.dir + file]
        images = load_and_preprocess_images(image_names).to(device)
        #print(file)

        with torch.no_grad():
            with torch.cuda.amp.autocast(dtype=dtype):
                # Predict attributes including cameras, depth maps, and point maps.
                predictions = model(images)
                #print(predictions)

       	        world_points = predictions["world_points"]
                fldName = os.path.basename(os.path.dirname(args.dir+ file))
                print(fldName)
                world_points_to_obj(world_points, filename=os.path.splitext(os.path.basename(file))[0], foldername=fldName, sample_stride=args.downsample)
                ball_pivot_mesh(fldName + "/" + os.path.splitext(os.path.basename(file)))

else:

    # Load and preprocess example images (replace with your own image paths)
    image_names = [args.input]
    images = load_and_preprocess_images(image_names).to(device)


    with torch.no_grad():
        with torch.cuda.amp.autocast(dtype=dtype):
            # Predict attributes including cameras, depth maps, and point maps.
            predictions = model(images)
            #print(predictions)
            print(predictions.keys())
            print(predictions["world_points"])

        
            world_points = predictions["world_points"]
            world_points_to_obj(world_points, sample_stride=args.downsample)
#           ball_pivot_mesh(world_points, "tomato.obj")
