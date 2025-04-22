import argparse
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

parser = argparse.ArgumentParser(description="This script generates search terms.")
parser.add_argument('--searches', type=int, help='How many search terms to generate.')
args = parser.parse_args()

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

prompt = "<|im_start|>system\nYou are Qwen, a helful assistant. "
prompt += "You will be asked to provide YouTube searches related to farming. "
prompt += "The searches relate to operating farm equiptment, planting crops, weeding, "
prompt += "and any other tasks a single person would be expected to do on a farm. "
prompt += "Give the search in the format SEARCH: <answer>. In other words, give your "
prompt += "final answer marked by SEARCH in all caps, a colon, then the search. "
prompt += "<|im_end|>\n"

prompt += "<|im_start|>user\nGive a search phrase related to farming:<|im_end|>\n"
prompt += "<|im_start|>assistant\nFinal Answer:\n"

o = model.generate(prompt, sampling_params=sampling_params)
print(o[0].outputs[0].text)

for i in range(args.searches - 1):
    prompt = "<|im_start|>user\nGive another search phrase related to farming:<|im_end|>\n"
    prompt += "<|im_start|>assistant\nFinal Answer:\n" 
    o = model.generate(prompt, sampling_params=sampling_params)
    print(o[0].outputs[0].text)
