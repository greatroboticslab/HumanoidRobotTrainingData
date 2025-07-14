import shutil
import os
import argparse

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--index', type=str, help='Video index.')
parser.add_argument('--frame', type=int, default=0, help='Copy from this frame.')

args = parser.parse_args()

os.makedirs("validation/" + args.index, exist_ok=True)

src_path = "../video_processing/frames/"+args.index+"/raw_frames/frame_"+str(args.frame).zfill(4)+".jpg"

dst_dir = os.getcwd()
dst_dir = os.path.join(dst_dir, "validation/" + args.index)
dst_path = os.path.join(dst_dir, "frame_"+str(args.frame).zfill(4)+".jpg")

# Check if it's a file before copying
if os.path.isfile(src_path):
    shutil.copy2(src_path, dst_path)

depth_path = "../depth_anything_baseline/output/"+args.index+"/depth_maps/frame_"+str(args.frame).zfill(4)+".png"

dst_path = os.path.join(dst_dir, "frame_"+str(args.frame).zfill(4)+".png")
if os.path.isfile(depth_path):
    shutil.copy2(depth_path, dst_path)


action_path = "../s1_baseline/output/"+args.index+".json"
dst_path = os.path.join(dst_dir, args.index+".json")
if os.path.isfile(action_path):
    shutil.copy2(action_path, dst_path)

caption_path = "../minicpm_baseline/captions/"+args.index+"/frame_"+str(args.frame).zfill(4)+".txt"
dst_path = os.path.join(dst_dir, "frame_"+str(args.frame).zfill(4)+".txt")
if os.path.isfile(caption_path):
    shutil.copy2(caption_path, dst_path)
