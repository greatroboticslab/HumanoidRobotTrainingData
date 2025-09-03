import bpy
import sys
import os

def main():
    # Get obj filepath from command line arguments
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # everything after "--"
    if not argv:
        print("Usage: blender --background --python unwrap_from_view.py -- /path/to/file.obj")
        return
    obj_path = os.path.abspath(argv[0])

    # Clear default scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Import OBJ
    bpy.ops.import_scene.obj(filepath=obj_path)

    # Ensure imported object is active
    obj = bpy.context.selected_objects[0]
    bpy.context.scene.objects.active = obj

    # Make sure we're in object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = obj.data

    # Create UV map if not exist
    if not mesh.uv_textures:
        mesh.uv_textures.new("UVMap")

    uv_layer = mesh.uv_layers.active.data

    # Collect X and Z coords (since we are projecting along -Y)
    xs, zs = [], []
    for v in mesh.vertices:
        xs.append(v.co.x)
        zs.append(v.co.z)

    min_x, max_x = min(xs), max(xs)
    min_z, max_z = min(zs), max(zs)
    scale_x = max_x - min_x
    scale_z = max_z - min_z

    # Assign UVs per loop (face corner)
    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            v_idx = mesh.loops[loop_index].vertex_index
            vx, vz = mesh.vertices[v_idx].co.x, mesh.vertices[v_idx].co.z
            u = (vx - min_x) / scale_x if scale_x != 0 else 0.5
            v = (vz - min_z) / scale_z if scale_z != 0 else 0.5
            uv_layer[loop_index].uv = (u, v)

    # Export back to obj (overwrite original)
    bpy.ops.export_scene.obj(filepath=obj_path, use_selection=True, use_materials=False)

if __name__ == "__main__":
    main()

