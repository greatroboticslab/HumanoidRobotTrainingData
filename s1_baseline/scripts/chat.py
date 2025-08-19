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

args = parser.parse_args()
model_name = "../" + args.model
_token_count = args.tokens
gpu_count = args.gpus

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
    return text.replace('relevantToken', relevantToken).replace('irrelevantToken', irrelevantToken)

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

startPrompt = "<|im_start|>system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>\n"

prompt = startPrompt

while(True):

    prompt += "<|im_start|>user\n"

    prompt += input("Enter Text: ")

    prompt += "<|im_end|>\n<|im_start|>assistant\nFinal Answer:\n"

    o = model.generate(prompt, sampling_params=sampling_params)
    print(o[0].outputs[0].text)
    lines = o[0].outputs[0].text.splitlines()
    prompt = ""
