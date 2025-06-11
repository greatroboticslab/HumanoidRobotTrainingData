from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import argparse

def main(args):
    # Replace with your Phi model's local path
    model_path = args.model_path

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    # Move to GPU if available
    model.to("cuda")

    
    with open(args.conversation_file, "r") as conversations:
        data = json.load(conversations)

    categorizations = [] 
    if args.subset:
        data = data[:args.subset]

    for conversation in data:
        conversationId = conversation["image"]
        print("Categorizing", conversationId)

        # Input and generation
        prompt = """
Below is a description of a graph's waveform and a multiple-choice question about it. Do not generate additional questions, answers, or options. Only respond directly to the final question. Only use the criteria below for your decision; do not use any outside knowledge.
        """
        for interaction in conversation["conversation"]:
            question = interaction["question"]
            answer = interaction["answer"]

            prompt += f"Question: {question}\nAnswer: {answer}\n"


        prompt += """\nThere are three options:

A) Random noise: Random noise waves have data points distributed randomly across the graph. Random noise waves have considerable value shifts. Random noise waves have rapid value alterations. Random noise waves do not have a discernible structure. 
B) Sine wave: Sine waves have gradual transitions from one level to another. Sine waves do not have rapid value alterations. Sine waves do not have any randomly distributed datapoints. Sine waves have an easily discernible structure.
C) Square wave: Square waves are not continuous. Square waves have sharp corners where it jumps from one value to another. If it lacks a discernible structure, it cannot be a square wave.

Final Question: Based on this information, which type of graph do I have? Only select from the three options (A, B, C) provided above. Do not invent new answers or modify the options. Explain your reasoning.
        """
        print(prompt)
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")

        outputs = model.generate(inputs, max_new_tokens = 200)

        # this is surprisingly weird to do?
        # https://github.com/huggingface/transformers/issues/17117#issuecomment-1120809167
        modelResponse = tokenizer.batch_decode(outputs[:, inputs.shape[1]:])[0]
    
        categorizations.append({"conversationId": conversationId, "response": modelResponse})
    
    with open(args.output_file, "w") as outputFile:
        json.dump(categorizations, outputFile, indent=2)

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--model-path", type=str, required=True)
    parse.add_argument("--conversation-file", type=str, required=True)
    parse.add_argument("--output-file", type=str, required=True)
    parse.add_argument("--subset", type=int)
    args = parse.parse_args()
    main(args)
