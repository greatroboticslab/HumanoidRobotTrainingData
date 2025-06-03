import argparse
import os
import subprocess
import caption_cpm

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--start', type=int, default=0, help='Start from this file #')
parser.add_argument('--end', type=int, default=-1, help='Stop processing at this file, set to -1 for all files from start.')

args = parser.parse_args()

frameDir = "../../video_processing/frames/"

onlyFolders = [name for name in os.listdir(frameDir) if os.path.isdir(os.path.join(frameDir, name))]

_from = args.start
if _from > len(onlyFolders):
    _from = len(onlyFolders)
_to = args.end
if _to > len(onlyFolders):
    _to = len(onlyFolders)
onlyFolders = onlyFolders[_from:_to]

# print(os.path.join(frameDir, onlyFolders[0]))

for f in onlyFolders:
    
    print("Processing " + f + "...")
    _f = f + "/raw_frames/"
    _folder = os.path.join(frameDir, _f)

    #result = subprocess.run(
    #    ["python", "caption_cpm.py", "--input_folder", f"{_folder}", "--output_folder", f"../captions/{_folder}"],
    #    capture_output=True, text=True, check=True
    #)

    caption_cpm.MakeCaptionsFromFolder(_folder, "../captions/" + f + "/")
