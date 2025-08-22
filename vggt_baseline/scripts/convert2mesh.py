import numpy as np
import open3d as o3d

def pointmap_to_mesh(point_map, out_file="mesh.ply"):
    """
    Convert VGGT point_map_by_unprojection (H, W, 3) into a triangle mesh.
    Saves the mesh as a .ply file.
    """

    H, W, _ = point_map.shape
    vertices = point_map.reshape(-1, 3)

    # Build faces (grid-based triangulation)
    faces = []
    for y in range(H - 1):
        for x in range(W - 1):
            i0 = y * W + x
            i1 = i0 + 1
            i2 = i0 + W
            i3 = i2 + 1
            # two triangles per cell
            faces.append([i0, i2, i1])
            faces.append([i1, i2, i3])

    faces = np.array(faces, dtype=np.int32)

    # Build Open3D mesh
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(faces)

    # Clean up (optional)
    mesh.remove_duplicated_vertices()
    mesh.remove_degenerate_triangles()
    mesh.compute_vertex_normals()

    # Save as .ply
    o3d.io.write_triangle_mesh(out_file, mesh)
    print(f"Mesh saved to {out_file}")

# ---------------- Example usage ----------------
if __name__ == "__main__":
    # Example: fake VGGT point_map
    H, W = 240, 320
    point_map = np.random.rand(H, W, 3)  # Replace with real VGGT output

    pointmap_to_mesh(point_map, "vggt_mesh.ply")
