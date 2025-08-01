import os
import shutil
import argparse
import random

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--count', type=int, default=1, help='Amount of sample folders to copy to this directory.')

args = parser.parse_args()

source_dir = os.path.abspath("../frames")
dest_dir = os.getcwd()

# Get all folders in source_dir
folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
#folders.sort()  # Optional: deterministic order

folders = random.sample(folders, args.count)

if args.count > len(folders):
    print(f"Requested {args.count} folders, but only found {len(folders)}.")
else:
    for folder in folders[:args.count]:
        src_path = os.path.join(source_dir, folder)
        dst_path = os.path.join(dest_dir, folder)
        print(f"Copying '{src_path}' to '{dst_path}'")
        shutil.copytree(src_path, dst_path)

