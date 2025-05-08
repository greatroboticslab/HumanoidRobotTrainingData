import json
import subprocess
import re

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

# Load the JSON file
with open('../s1_baseline/output/output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract tasks

for item in data:
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
        for st in _subtasks:
            try:
                print("+-> Generating subtask: " + folderName + "/" + st)
                result = subprocess.run(["conda", "run", "-n", "momask", "python", "gen_t2m.py", "--gpu_id", "0", "--ext", f"batch_motions/{folderName}", "--text_prompt", st],capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                print("Command failed:")
                print("STDOUT:", e.stdout)
                print("STDERR:", e.stderr)
                raise
