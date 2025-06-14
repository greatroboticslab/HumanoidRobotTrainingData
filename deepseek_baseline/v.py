from vllm import LLM, SamplingParams

prompts = [
    "{question}What is the capital of France?"
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

#llm = LLM(model="DeepSeek-R1-Distill-Qwen-7B", dtype="half")
#llm = LLM(model="DeepSeek-R1-Distill-Qwen-7B")
llm = LLM(model="DeepSeek-R1-Distill-Qwen-32B")

outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

