import os
import shutil
import argparse
import random

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--count', type=int, default=10, help='Amount of sample folders to copy to this directory.')

args = parser.parse_args()

source_dir = os.path.abspath("../output/tasks/")
dest_dir = os.getcwd()

# Get all folders in source_dir
folders = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
#folders.sort()  # Optional: deterministic order

smallest = args.count
if smallest > len(folders):
    smallest = len(folders)

folders = random.sample(folders, smallest)

if args.count > len(folders):
    print(f"Requested {args.count} folders, but only found {len(folders)}.")

for i in range(smallest):
    src_path = os.path.join(source_dir, folders[i])
    dst_path = os.path.join(dest_dir, folders[i])
    if i < len(folders):
        print(f"Copying '{src_path}' to '{dst_path}'")
        shutil.copy(src_path, dst_path)
