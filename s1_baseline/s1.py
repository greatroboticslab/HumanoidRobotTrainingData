import argparse
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import shutil

import os
import json
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--model', type=str, default="s1.1-7B", help='Name or path of the model')
parser.add_argument('--gpus', type=int, default=4, help='Number of GPUs to use.')
parser.add_argument('--tokens', type=int, default=32768, help='Max number of tokens.')
args = parser.parse_args()
model_name = args.model
_token_count = args.tokens
gpu_count = args.gpus

irrelevantToken = "!!!TRANSCRIPT_IRRELEVANT:"
relevantToken = ">>>ACCEPT:"
YOUTUBE_PREFIX = "https://www.youtube.com/watch?v="

def IsSubtask(line):
    if "SUBTASK" in line:
        return True
    return False

def ExtractTask(line):
    if irrelevantToken in line:
        return irrelevantToken
    if relevantToken in line:
        return relevantToken
    if "MAINTASK" in line:
        return line
    if "SUBTASK" in line:
        return line
    return "null"

def GetRelevantReason(line):
    if relevantToken in line:
        return line.split(relevantToken, 1)[1].strip()
    return ""

def GetIrrelevantReason(line):
    if irrelevantToken in line:
        return line.split(irrelevantToken, 1)[1].strip()
    return ""

def TaskToMoMask(line):
    if ':' in line:
        return line.split(':', 1)[1].strip()
    return line.strip()


filenames = []
blacklist = ""

model = LLM(
    model_name,
    max_model_len=_token_count,
    tensor_parallel_size=gpu_count,
    disable_custom_all_reduce=True
)
tok = AutoTokenizer.from_pretrained(model_name)

stop_token_ids = tok("<|im_end|>")["input_ids"]

sampling_params = SamplingParams(
    max_tokens=32768,
    min_tokens=0,
    stop_token_ids=stop_token_ids,
)

mypath = "../video_processing/transcripts/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
jsonData = []
allTasks = []
allSubtasks = []
relevantCount = 0
irrelevantCount = 0
whitelist = []
whitelist_titles = []
whitelist_categories = []
whitelist_reasons = []

for file in onlyfiles:

    if(str(file[0]) != '.'):
        if True: #try:
            tasks = []
            #print(str(file[0]))
            #print(str(file))
            fi = open(mypath + file, "r", encoding="ascii", errors="ignore")

            vID = os.path.splitext(file)[0]
            url = YOUTUBE_PREFIX + vID
            videoTitle = "Unknown Title"
            videoCategory = "Unknown Category"
            reason = "Video is relevant to farming and agriculture."
            rejectionReason = "Scripting error."
            relevant = True
            transcriptLines = []
            try:
                transcriptLines = fi.readlines()
                videoTitle = transcriptLines[0].replace('\n', '').replace('\r', '')
                videoCategory = transcriptLines[2].replace('\n', '').replace('\r', '')
                transcript = ""
                for i in range(3, len(transcriptLines)):
                    transcript += transcriptLines[i] + "\n"

                prompt = "<|im_start|>system\nYou are Qwen, a helful assistant. "
                prompt += "You will be given a video transcript and asked to generate a series of tasks "
                prompt += "based on the transcript that a person would have to perform. "
                prompt += "A task should be a generalization, and made up of smaller sub-tasks. "
                prompt += "Give one task per line. Write MAINTASK: before every task. "
                prompt += "After writing MAINTASK: give a list of subtasks, one per line. "
                prompt += "A for each subtask, write SUBTASK: before every subtask. "
                prompt += "When you are finished with the subtasks for a task, you can start "
                prompt += "a new task by writing MAINTASK: and then the new general task. "
                prompt += "Give only tasks and subtasks, do not discuss or talk about anything else. "
                prompt += "Do not go into detail on how you made each task, just give the tasks. "
                prompt += "Only include tasks and subtasks that are related to farming, agriculture, or operating farming equiptment."
                prompt += "However, if you feel that the transcript has nothing to do with the tasks of performing physical farming, husbandry, or agricultural tasks, then simply say " + irrelevantToken + " all caps, with 3 exclamation points at the beginning, followed by the reason for the video being irrelevant. "
                prompt += "Do not forget to include the reason after the colon if the video transcript is irrelevant. "
                prompt += "The entire transcript must be irrelevant. Otherwise, if it is still somewhat relevant, just save the tasks of the relevant actions, and do not write " + irrelevantToken + ". "
                prompt += "At the end, if the video transcript is relevant (you have not said " + irrelevantToken + "), put " + relevantToken + " followed by the reason the video is relevant."
                prompt += "<|im_end|>\n"
                prompt += "<|im_start|>user\nGiven this transcript, please generate a list of physical tasks a person would have to perform with their body in relation to the transcript. Separate the tasks by a new line character:"
            
                prompt += transcript

                prompt += "<|im_end|>\n<|im_start|>assistant\nFinal Answer:\n"
                #prompt = "<|im_start|>system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>\n<|im_start|>user\n" + prompt + "<|im_end|>\n<|im_start|>assistant\n"

                o = model.generate(prompt, sampling_params=sampling_params)
                #print(o[0].outputs[0].text)
                lines = o[0].outputs[0].text.splitlines()
                
                curTask = -1
                for l in lines:
                    task = ExtractTask(l)
                    if task != "null":
                        if task == irrelevantToken:
                            # Reject
                            relevant = False
                            rejectionReason = GetIrrelevantReason(l).replace(',', '')
                        else:
                            if task == relevantToken:
                                reason = GetRelevantReason(l).replace(',', '')
                                
                            else:
                                # Accept
                        
                                # print(l)
                                motion = TaskToMoMask(task)
                                if IsSubtask(l):
                                    if len(tasks) > 0:
                                        tasks[curTask].append(motion)
                                else:
                                    newTask = [motion]
                                    tasks.append(newTask)
                                    curTask += 1
                                
                                # tasks.append(motion)
                            
                
            except Exception as e:
                relevant = False
                print("File Error: ", e)
                

            if relevant:
                print(str(file) + ": relevant video (" + reason + "), saving tasks...")
                whitelist.append(vID)
                whitelist_titles.append(videoTitle)
                whitelist_categories.append(videoCategory)
                whitelist_reasons.append(reason)
                relevantCount += 1
                for t in tasks:
                    for s in t:
                        allTasks.append(s)

                # Output info CSV
                
                jTasks = []
                for t in tasks:
                    jTask = {
                         "task": t[0],
                         "subtasks": t[1:]
                    }
                    jTasks.append(jTask)

                entry = {
                    "index": vID,
                    "title": videoTitle,
                    "url": url,
                    "category": videoCategory,
                    "tasks": jTasks
                }
                jsonData.append(entry)

            else:
                print(str(file) + ": irrelevant video (" + rejectionReason + "), blacklisting...")
                irrelevantCount += 1
                blacklist += url + ", " + rejectionReason + "\n"

jsonFile = open("output/output.json", "w")
json.dump(jsonData, jsonFile, indent=4)
jsonFile.close()

# outputFile = open("output/momask_tasks.txt", "w", encoding="ascii", errors="ignore")
# outputString = ""
# for t in allTasks:
#     outputString += t + '#NA\n'
# outputFile.write(outputString)
# outputFile.close()

blacklistFile = open("../video_processing/blacklist.txt", "w")
blacklistFile.write(blacklist)
blacklistFile.close()

print("Saved output from " + str(relevantCount) + " videos.")
print("Ignoring " + str(irrelevantCount) + " irrelevant videos.")

# Copy over videos
print("Copying relevant videos to relevant_videos/")
for w in whitelist:
    shutil.copy("../video_processing/rawvideos/" + w + ".mp4", "../video_processing/relevant_videos/"+w+".mp4")

# Save CSV File
csvFile = open("../video_processing/relevant_videos/video_data.csv", "w")
cLines = "index, url, video title, category, reason\n"
for i in range(len(whitelist)):
    cLines += str(whitelist[i]) + ", https://www.youtube.com/watch?v=" + whitelist[i] + ", " + whitelist_titles[i] + ", " + whitelist_categories[i] + ", " + whitelist_reasons[i] + "\n"
csvFile.write(cLines)
csvFile.close()
