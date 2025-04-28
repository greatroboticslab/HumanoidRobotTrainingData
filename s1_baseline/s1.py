from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

import os
import json
from os import listdir
from os.path import isfile, join

irrelevantToken = "!IRRELEVANT!"
YOUTUBE_PREFIX = "https://www.youtube.com/watch?v="

def ExtractTask(line):
    if irrelevantToken in line:
        return irrelevantToken
    if "TASK" in line:
        return line
    return "null"

def TaskToMoMask(line):
    if ':' in line:
        return line.split(':', 1)[1].strip()
    return line.strip()


filenames = []
blacklist = ""

model = LLM(
    "s1.1-7B",
    tensor_parallel_size=4,
    disable_custom_all_reduce=True
)
tok = AutoTokenizer.from_pretrained("s1.1-7B")

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
relevantCount = 0
irrelevantCount = 0

for file in onlyfiles:

    if(str(file[0]) != '.'):
        if True: #try:
            tasks = []
            print(str(file[0]))
            print(str(file))
            fi = open(mypath + file, "r", encoding="ascii", errors="ignore")

            vID = os.path.splitext(file)[0]
            url = YOUTUBE_PREFIX + vID
            videoTitle = "Unknown Title"
            relevant = True
            transcriptLines = []
            try:
                transcriptLines = fi.readlines()
                videoTitle = transcriptLines[0]
                transcript = ""
                for i in range(2, len(transcriptLines)):
                    transcript += transcriptLines[i] + "\n"

                prompt = "<|im_start|>system\nYou are Qwen, a helful assistant. "
                prompt += "You will be given a video transcript and asked to generate a series of tasks "
                prompt += "based on the transcript that a person would have to perform. "
                prompt += "Give one task per line. Write TASK: before every task. "
                prompt += "Give tasks and only tasks, do not discuss or talk about anything else. "
                prompt += "Do not go into detail on how you made each task, just give the tasks. "
                prompt += "Only include tasks that are related to farming, agriculture, or operating farming equiptment."
                prompt += "However, if you feel that the transcript has nothing to do with the tasks of performing physical farming tasks, then simply say " + irrelevantToken + " all caps, exclamation points surrounding it. "
                prompt += "The entire transcript must be irrelevant. If it is still somewhat relevant, just save the tasks of the relevant actions."
                prompt += "<|im_end|>\n"
                prompt += "<|im_start|>user\nGiven this transcript, please generate a list of physical tasks a person would have to perform with their body in relation to the transcript. Separate the tasks by a new line character:"
            
                prompt += transcript

                prompt += "<|im_end|>\n<|im_start|>assistant\nFinal Answer:\n"
                #prompt = "<|im_start|>system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>\n<|im_start|>user\n" + prompt + "<|im_end|>\n<|im_start|>assistant\n"

                o = model.generate(prompt, sampling_params=sampling_params)
                #print(o[0].outputs[0].text)
                lines = o[0].outputs[0].text.splitlines()

                for l in lines:
                    task = ExtractTask(l)
                    if task != "null":
                        if task == irrelevantToken:
                            # Reject
                            relevant = False
                        else:
                            # Accept
                        
                            print(l)
                            motion = TaskToMoMask(task)
                            tasks.append(motion)
                            
                
            except:
                relevant = False
                print("File IO error, skipping...")
                

            if relevant:
                print("Relevant video, saving tasks...")
                relevantCount += 1
                for t in tasks:
                    allTasks.append(t)

                # Output info CSV
                
                entry = {
                    "index": vID,
                    "title": videoTitle,
                    "url": url,
                    "tasks": tasks
                }
                jsonData.append(entry)

            else:
                print("Irrelevant video, blacklisting...")
                irrelevantCount += 1
                blacklist += url + "\n"

jsonFile = open("output/output.json", "w")
json.dump(jsonData, jsonFile, indent=4)
jsonFile.close()

outputFile = open("output/momask_tasks.txt", "w", encoding="ascii", errors="ignore")
outputString = ""
for t in allTasks:
    outputString += t + '#NA\n'
outputFile.write(outputString)
outputFile.close()

blacklistFile = open("blacklist.txt", "w")
blacklistFile.write(blacklist)
blacklistFile.close()

print("Saved output from " + str(relevantCount) + " videos.")
print("Ignoring " + str(irrelevantCount) + " irrelevant videos.")
