import subprocess
import os

def list_obj_files(root_dir="../output"):
    obj_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith(".obj"):
                full_path = os.path.abspath(os.path.join(dirpath, f))
                obj_files.append(full_path)
    return obj_files

if __name__ == "__main__":
    obj_files = list_obj_files()
    for path in obj_files:
        print(path)
        newPath = path.replace("/output/", "/meshes/", 1)
        cmd = [
            "meshlabserver",
            "-i", path,
            "-o", newPath,
            "-s", "remesh.mlx"
        ]
        subprocess.run(cmd, check=True)
