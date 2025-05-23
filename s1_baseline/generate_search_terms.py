import argparse
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

def extract_search_text(input_str):
    keyword = "SEARCH:"
    start = input_str.find(keyword)
    
    if start == -1:
        return None  # or return "" if you prefer empty string instead
    
    # Move past "SEARCH:"
    start += len(keyword)
    
    # Get the remaining string after SEARCH:
    remaining = input_str[start:].lstrip()
    
    # Stop at the first newline if it exists
    end = remaining.find('\n')
    
    if end != -1:
        return remaining[:end].strip()
    else:
        return remaining.strip()

parser = argparse.ArgumentParser(description="This script generates search terms.")
parser.add_argument('--searches', type=int, help='How many search terms to generate.')
parser.add_argument('--model', type=str, default="s1.1-7B", help='Name or path of the model')
parser.add_argument('--gpus', type=int, default=4, help='Number of GPUs to use.')
parser.add_argument('--tokens', type=int, default=4096, help='Max number of tokens.')
parser.add_argument('--save_interval', type=int, default=150, help='Save the progress every save_interval generations.')
args = parser.parse_args()
model_name = args.model
_token_count = args.tokens
gpu_count = args.gpus
saveEveryXVideos = args.save_interval

model = LLM(
    model_name,
    tensor_parallel_size=gpu_count,
    disable_custom_all_reduce=True
)
tok = AutoTokenizer.from_pretrained(model_name)

stop_token_ids = tok("<|im_end|>")["input_ids"]

sampling_params = SamplingParams(
    max_tokens=_token_count,
    min_tokens=0,
    stop_token_ids=stop_token_ids,
)

prompt = "<|im_start|>system\nYou are Qwen, a helful assistant. "
prompt += "You will be asked to provide YouTube searches related to farming. "
prompt += "The searches relate to operating farm equiptment, planting crops, weeding, "
prompt += "and any other tasks a single person would be expected to do on a farm. "
prompt += "Give the search in the format SEARCH: <answer>. In other words, give your "
prompt += "final answer marked by SEARCH in all caps, a colon, then the search. "
prompt += "Be sure to include the SEARCH: at the end of your answer. "
prompt += "<|im_end|>\n"

prompt += "<|im_start|>user\nGive a search phrase related to farming:<|im_end|>\n"
prompt += "<|im_start|>assistant\nFinal Answer:\n"

searches = []

o = model.generate(prompt, sampling_params=sampling_params)
print(str(extract_search_text(o[0].outputs[0].text)))
print("==============")

searches.append(str(extract_search_text(o[0].outputs[0].text)))

def SaveFile(_s):
    outString = ""
    for s in _s:
        outString += s + "\n"
    outFile = open("../video_processing/output/video_downloading/search_terms.txt", "w")
    outFile.write(outString.encode('ascii', 'ignore').decode('ascii'))
    outFile.close()

for i in range(args.searches - 1):
    prompt = "<|im_start|>user\nGive another search phrase related to farming. "
    prompt += "Be sure to include the SEARCH: and the search phrase after at the end of your answer.<|im_end|>\n"
    prompt += "<|im_start|>assistant\nFinal Answer:\n" 
    o = model.generate(prompt, sampling_params=sampling_params)
    print(str(extract_search_text(o[0].outputs[0].text)))
    print("==============")
    searches.append(str(extract_search_text(o[0].outputs[0].text)))

    if (i + 1) % saveEveryXVideos == 0:
        SaveFile(searches)

SaveFile(searches)
