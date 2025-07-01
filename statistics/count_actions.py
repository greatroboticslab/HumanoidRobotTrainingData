import os
import json

def count_tasks_and_subtasks(directory):
    total_tasks = 0
    total_subtasks = 0

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                    tasks = data.get("tasks", [])
                    total_tasks += len(tasks)
                    for task in tasks:
                        subtasks = task.get("subtasks", [])
                        total_subtasks += len(subtasks)
                except json.JSONDecodeError as e:
                    print(f"Error parsing {filename}: {e}")

    print("Total tasks:", total_tasks)
    print("Total subtasks:", total_subtasks)

# Example usage:
count_tasks_and_subtasks("../s1_baseline/output/")
