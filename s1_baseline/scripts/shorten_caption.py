import argparse
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import shutil
import csv

import os
import json
from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--model', type=str, default="s1.1-7B", help='Name or path of the model')
parser.add_argument('--gpus', type=int, default=4, help='Number of GPUs to use.')
parser.add_argument('--tokens', type=int, default=32768, help='Max number of tokens.')
parser.add_argument('--start', type=int, default=0, help='Start from this file #')
parser.add_argument('--end', type=int, default=-1, help='Stop processing at this file, set to -1 for all files from start.')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')

args = parser.parse_args()
model_name = "../" + args.model
_token_count = args.tokens
gpu_count = args.gpus

irrelevantToken = "!!!TRANSCRIPT_IRRELEVANT:"
relevantToken = ">>>ACCEPT:"
finalToken = ">>>FINAL_CAPTION:"
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

def SubstituteTokens(text: str) -> str:
    return text.replace('finalToken', finalToken)

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

mypath = "../../video_processing/minicpm_captions/"
onlyfiles = [f for f in os.listdir(mypath) if os.path.isdir(os.path.join(mypath, f))]
print(onlyfiles)
_from = args.start
if _from > len(onlyfiles):
    _from = len(onlyfiles)
_to = args.end
if _to > len(onlyfiles):
    _to = len(onlyfiles)
onlyfiles = onlyfiles[_from:_to]
jsonData = []
allTasks = []
allSubtasks = []
relevantCount = 0
irrelevantCount = 0
whitelist = []
whitelist_titles = []
whitelist_categories = []
whitelist_reasons = []

#print(onlyfiles)

if args.debug:
    dFile = open("../../debug/testdata/videorelevancetest.txt", "r")
    dLines = dFile.readlines()
    for l in range(len(dLines)):
        dLines[l] = dLines[l][:-1]+".txt"
    print(dLines)

    onlyfiles = dLines

print(onlyfiles)

for _folder in onlyfiles:

    folder = mypath + _folder
    print(folder)

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    print(files)

    for file in files:

        if(str(file[0]) != '.'):
            if True: #try:
                tasks = []
                #print(str(file[0]))
                #print(str(file))
                fi = open(folder + "/" + file, "r", encoding="ascii", errors="ignore")

                vID = os.path.basename(os.path.normpath(folder))
                url = YOUTUBE_PREFIX + vID
                videoTitle = "Unknown Title"
                videoCategory = "Unknown Category"
                reason = "Video is relevant to farming and agriculture."
                rejectionReason = "Scripting error."
                relevant = True
                transcriptLines = []
                try:
                    print(file)
                    transcriptLines = fi.readlines()
                    #print(transcriptLines)
                    #videoTitle = transcriptLines[0].replace('\n', '').replace('\r', '')
                    #videoCategory = transcriptLines[2].replace('\n', '').replace('\r', '')
                    transcript = ""
                    for i in range(0, len(transcriptLines)):
                        transcript += transcriptLines[i] + "\n"

                    promptFile = open("caption_prompt.txt", "r")
                    prompt = SubstituteTokens(promptFile.read())
                    promptFile.close()

                    #print("!! 1")

                    #prompt = "<|im_start|>system\nYou are Qwen, a helful assistant. "
                    #prompt += "You will be given a video transcript and asked to generate a series of tasks "
                    #prompt += "based on the transcript that a person would have to perform. "
                    #prompt += "A task should be a generalization, and made up of smaller sub-tasks. "
                    #prompt += "Give one task per line. Write MAINTASK: before every task. "
                    #prompt += "After writing MAINTASK: give a list of subtasks, one per line. "
                    #prompt += "A for each subtask, write SUBTASK: before every subtask. "
                    #prompt += "When you are finished with the subtasks for a task, you can start "
                    #prompt += "a new task by writing MAINTASK: and then the new general task. "
                    #prompt += "Give only tasks and subtasks, do not discuss or talk about anything else. "
                    #prompt += "Do not go into detail on how you made each task, just give the tasks. "
                    #prompt += "Only include tasks and subtasks that are related to farming, agriculture, or operating farming equiptment."
                    #prompt += "However, if you feel that the transcript has nothing to do with the tasks of performing physical farming, husbandry, or agricultural tasks, then simply say " + irrelevantToken + " all caps, with 3 exclamation points at the beginning, followed by the reason for the video being irrelevant. "
                    #prompt += "Do not forget to include the reason after the colon if the video transcript is irrelevant. "
                    #prompt += "The entire transcript must be irrelevant. Otherwise, if it is still somewhat relevant, just save the tasks of the relevant actions, and do not write " + irrelevantToken + ". "
                    #prompt += "At the end, if the video transcript is relevant (you have not said " + irrelevantToken + "), put " + relevantToken + " followed by the reason the video is relevant."
                    #prompt += "<|im_end|>\n"
                    #prompt += "<|im_start|>user\nGiven this transcript, please generate a list of physical tasks a person would have to perform with their body in relation to the transcript. Separate the tasks by a new line character:"
            
                    prompt += transcript

                    prompt += "<|im_end|>\n<|im_start|>assistant\nFinal Answer:\n"
                    #prompt = "<|im_start|>system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>\n<|im_start|>user\n" + prompt + "<|im_end|>\n<|im_start|>assistant\n"

                    o = model.generate(prompt, sampling_params=sampling_params)
                    #print("Output: ")
                    #print(o[0].outputs[0].text)
                    lines = o[0].outputs[0].text.splitlines()
                    caption = ""
                    found = False

                    #print("!! 2")

                    for l in lines:
                        #Fix for if caption is on the next line
                        if found and len(caption) < 3:
                            caption = l
                            #print("--Updating caption to: " + l)
                        #print(l)
                        if finalToken in l:
                            #print("IN LINE!!!")
                            #print("!! 3")
                            caption = l.split(finalToken, 1)[1].strip()
                            #print("--Caption is currently: " + caption + " | (" + str(len(caption)) + ")")
                            found = True

                    if caption != "" and len(caption) < len(transcript):
                        print("Final Caption: " + caption)
                    else:
                        caption = transcript
                        print("No caption generated! Using original: " + transcript)

                    os.makedirs("../../minicpm_baseline/output/shortencaptions/" + vID + "/", exist_ok=True)
                    outFile = open("../../minicpm_baseline/output/shortencaptions/" + vID + "/" + file, "w")
                    outFile.write(caption)
                    outFile.close()

                except Exception as e:
                    relevant = False
                    print("File Error: ", e)
