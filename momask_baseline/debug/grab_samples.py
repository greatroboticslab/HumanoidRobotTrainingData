import os
import shutil
import argparse
import random

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--count', type=int, default=10, help='Amount of sample folders to copy to this directory.')

args = parser.parse_args()

source_dir = os.path.abspath("../generation/batch_motions/")
dest_dir = os.getcwd()

# Get all folders in source_dir
categories = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]

folders = []

for c in categories:
    sub_dir = os.path.abspath("../generation/batch_motions/" + c + "/")
    fs = [f for f in os.listdir(sub_dir) if os.path.isdir(os.path.join(sub_dir, f))]
    for _f in fs:
        folders.append(c + "/" + _f)

#folders.sort()  # Optional: deterministic order

smallest = args.count
if smallest > len(folders):
    smallest = len(folders)

folders = random.sample(folders, smallest)

if args.count > len(folders):
    print(f"Requested {args.count} folders, but only found {len(folders)}.")

for i in range(smallest):
    src_path = os.path.join(source_dir, folders[i])
    fName = os.path.normpath(folders[i])
    fName = os.path.basename(fName)
    dst_path = os.path.join(dest_dir, fName)
    if i < len(folders):
        print(f"Copying '{src_path}' to '{dst_path}'")
        shutil.copytree(src_path, dst_path)
