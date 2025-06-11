import torch
from transformers import pipeline
import argparse
import json
import pandas as pd


def main(args):
    # Replace with your Phi model's local path
    model_path = args.model_path
    answer = f"{args.answer})"

    pipe = pipeline(
        "text-generation",
        model=model_path,
        torch_dtype=torch.bfloat16,
        pad_token_id=128001,
    )
    # Load tokenizer and model
    
    with open(args.conversation_file, "r") as conversations:
        data = json.load(conversations)
    print(data[0])
    if args.subset:
        data = data[:args.subset]
    images = []
    results = []
    answers = []
    for row in data:
        conversationId = row["conversationId"]
        images.append(conversationId)
        print("Categorizing", conversationId)
        if row["response"][:100].find(answer) != -1:
            results.append(1)
            answers.append(answer)
            print("Found it!")
        else:
        # Input and generation
            prompt = """
    Below is an answer to a multiple choice question with an explanation. The answer will be in the format of A), B), or C). Provide only the answer - no other explanation. 
    """
            prompt += row["response"]
            messages = [{"role": "system", 
                "content": "You categorize answers. Provide only the final answer."}, 
                {"role": "user", "content": prompt}]
            outputs = pipe(
                messages,
                max_new_tokens=256,
            ) 
            modelResponse = outputs[0]["generated_text"][-1]["content"]
            print(modelResponse)
            answers.append(modelResponse)
            if modelResponse.find(answer) != -1:
                results.append(1)
            else:
                results.append(0)


    data = pd.DataFrame({"image": images, "result": results, "answer": answers})
    data.to_csv(args.output_file, index=False)

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--model-path", type=str, required=True)
    parse.add_argument("--conversation-file", type=str, required=True)
    parse.add_argument("--output-file", type=str, required=True)
    parse.add_argument("--subset", type=int)
    parse.add_argument("--answer", type=str, required=True)
    args = parse.parse_args()
    main(args)
