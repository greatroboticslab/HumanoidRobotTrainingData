import subprocess
import sys
import os

def list_obj_files(root_dir="../output"):
    obj_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith(".obj"):
                full_path = os.path.abspath(os.path.join(dirpath, f))
                obj_files.append(full_path)
    return obj_files


def normalize(values):
    """Normalize a list of values to range [0,1]."""
    min_val = min(values)
    max_val = max(values)
    if max_val == min_val:  # avoid division by zero
        return [0.5 for _ in values]
    return [(v - min_val) / (max_val - min_val) for v in values]

def generate_uvs(vertices):
    """Generate UVs from x and z coordinates of vertices."""
    x = 0.4
    xs = [v[0]*(v[2]*x) for v in vertices]
    zs = [v[1]*(v[2]*x) for v in vertices]
    u_coords = normalize(xs)
    v_coords = normalize(zs)
    return list(zip(u_coords, v_coords))

def process_obj(input_path, output_path):
    vertices = []
    faces = []
    other_lines = []

    # Read the .obj
    with open(input_path, 'r') as f:
        for line in f:
            if line.startswith("v "):  # vertex
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                vertices.append((x, y, z))
            elif line.startswith("f "):  # face
                parts = line.strip().split()[1:]
                faces.append(parts)
            else:
                other_lines.append(line.rstrip("\n"))

    # Generate UVs
    uvs = generate_uvs(vertices)

    # Write new OBJ
    with open(output_path, 'w') as f:
        for line in other_lines:
            f.write(line + "\n")

        # Write vertices
        for v in vertices:
            f.write("v {:.6f} {:.6f} {:.6f}\n".format(*v))

        # Write UVs
        for uv in uvs:
            f.write("vt {:.6f} {:.6f}\n".format(uv[0], uv[1]))

        # Write faces (with UV indices)
        for face in faces:
            new_face = []
            for idx in face:
                # Some faces may have v/vt/vn or v//vn format, handle that
                v_parts = idx.split("/")
                v_idx = int(v_parts[0])
                vt_idx = v_idx  # since we made one UV per vertex
                if len(v_parts) == 1:
                    new_face.append(f"{v_idx}/{vt_idx}")
                elif len(v_parts) == 2:
                    new_face.append(f"{v_idx}/{vt_idx}")
                elif len(v_parts) == 3:
                    vn = v_parts[2]
                    new_face.append(f"{v_idx}/{vt_idx}/{vn}")
            f.write("f " + " ".join(new_face) + "\n")


if __name__ == "__main__":
    obj_files = list_obj_files()
    for path in obj_files:
        print(path)
        newPath = path.replace("/output/", "/meshes/", 1)
        os.makedirs(os.path.dirname(newPath), exist_ok=True)
        cmd = [
            "meshlabserver",
            "-i", path,
            "-o", newPath,
            "-s", "remesh.mlx"
        ]
        try:
            subprocess.run(cmd, check=True)
            
            process_obj(newPath, newPath)
            
        except Exception as e:
            print("Error remeshing file: " + path)
            print(e)
