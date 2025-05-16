from os import listdir
from os.path import isfile, join
import argparse
import json
import subprocess
import re

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--start', type=int, default=0, help='Start from this file #')
parser.add_argument('--end', type=int, default=-1, help='Stop processing at this file, set to -1 for all files from start.')
args = parser.parse_args()

def sanitize_folder_name(name: str) -> str:
    # Strip leading/trailing whitespace
    name = name.strip()

    # Replace invalid characters (Windows: <>:"/\|?*, Linux: /)
    invalid_chars = r'[<>:"/\\|?*\']'
    name = re.sub(invalid_chars, '_', name)

    # Remove control characters (ASCII codes 0–31)
    name = ''.join(c for c in name if ord(c) >= 32)

    # Remove trailing periods or spaces (not allowed in Windows)
    name = name.rstrip(' .')

    # Optional: truncate if too long (max path is 255 chars, keep folder name conservative)
    max_length = 100
    if len(name) > max_length:
        name = name[:max_length]

    return name



# Extract tasks

mypath = "../s1_baseline/output/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

_from = args.start
if _from > len(onlyfiles):
    _from = len(onlyfiles)
_to = args.end
if _to > len(onlyfiles):
    _to = len(onlyfiles)

onlyfiles = onlyfiles[_from:_to]

for vid in onlyfiles:

    data = None

    # Load the JSON file
    print("Loading " + str(vid) + "...")
    with open("../s1_baseline/output/" + str(vid), 'r', encoding='utf-8') as f:
        data = json.load(f)

    item = data
    tasks = []
    category = item.get("category")
    index = item.get("index")
    curFolder = str(category) + "/" + index + "/"
    for task_block in item.get("tasks", []):
        task_description = task_block.get("task")
        subtasks = task_block.get("subtasks", [])
        tasks.append([task_description] + subtasks)

    for t in tasks:
        #folderName = sanitize_folder_name(t[0])
        folderName = curFolder + sanitize_folder_name(t[0])
        _subtasks = t[1:]
        # If no subtasks, just use the main task
        if len(_subtasks) < 1:
            _subtasks = []
            _subtasks.append(t[0])
        print("Task: " + t[0])
        for st in _subtasks:
            try:
                _folderName = folderName + "/" + sanitize_folder_name(st)
                if len(st) > 3:
                    print("\t+-> Generating subtask: " + _folderName)
                    result = subprocess.run(["conda", "run", "-n", "momask", "python", "gen_t2m.py", "--gpu_id", "0", "--ext", f"batch_motions/{_folderName}", "--text_prompt", st],capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                print("Command failed:")
                print("STDOUT:", e.stdout)
                print("STDERR:", e.stderr)
