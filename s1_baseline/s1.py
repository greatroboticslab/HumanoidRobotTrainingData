from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

from os import listdir
from os.path import isfile, join

def ExtractTask(line):
    if "TASK" in line:
        return line
    return "null"

tasks = []

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

for file in onlyfiles:

    if(str(file[0]) != '.'):
        print(str(file[0]))
        print(str(file))
        fi = open(mypath + file, "r")

        prompt = "<|im_start|>system\nYou are Qwen, a helful assistant. "
        prompt += "You will be given a video transcript and asked to generate a series of tasks "
        prompt += "based on the transcript that a person would have to perform. "
        prompt += "Give one task per line. Write TASK: before every task. "
        prompt += "Give tasks and only tasks, do not discuss or talk about anything else. "
        prompt += "Do not go into detail on how you made each task, just give the tasks. "
        prompt += "Only include tasks that are related to farming, agriculture, or operating farming equiptment."
        prompt += "<|im_end|>\n"
        prompt += "<|im_start|>user\nGiven this transcript, please generate a list of physical tasks a person would have to perform with their body in relation to the transcript. Separate the tasks by a new line character:"
        prompt += fi.read() # .encode('ascii','ignore')
        prompt += "<|im_end|>\n<|im_start|>assistant\nFinal Answer:\n"
        #prompt = "<|im_start|>system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>\n<|im_start|>user\n" + prompt + "<|im_end|>\n<|im_start|>assistant\n"

        o = model.generate(prompt, sampling_params=sampling_params)
        #print(o[0].outputs[0].text)
        lines = o[0].outputs[0].text.splitlines()
        for l in lines:
            task = ExtractTask(l)
            if task != "null":
                print(l)
                tasks.append(l)
