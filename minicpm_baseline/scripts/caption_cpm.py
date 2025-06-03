import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
from transformers import AutoModelForCausalLM
import os
import argparse



# Function to generate caption and return a string caption
def generate_caption(image_path):
    # Load the model and tokenizer
    
    model = AutoModelForCausalLM.from_pretrained(
        'openbmb/MiniCPM-V',
        trust_remote_code=True,
        torch_dtype=torch.float32  # Use float32 for CPU compatibility
    )
    # Set to GPU if available; otherwise, use CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V', trust_remote_code=True)
    model.eval()

    # Load and preprocess the image
    try:
        image = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Prepare the input question
    question = 'our caption is too short,please show detailed and overview for the image.'
    msgs = [{'role': 'user', 'content': question}]
    context = "This is an image captioning task."

    # Generate the caption using the model
    try:
        res = model.chat(
            image=image,
            context=context,
            msgs=msgs,
            tokenizer=tokenizer,
            sampling=True,  # If sampling=False, beam_search will be used by default
            temperature=0.7
        )
    except Exception as e:
        print(f"Error generating caption: {e}")
        return

    generated_caption = res[0]  # Assuming res returns a string with the generated caption

    return generated_caption

def MakeCaptionFile(oFolder, fName, caption):
    os.makedirs(oFolder, exist_ok=True)
    outputFilePath = os.path.join(oFolder, fName) + ".txt"
    cFile = open(outputFilePath, "w")
    cFile.write(caption)
    cFile.close()

def MakeCaptionsFromFolder(_inputFolder, _outputFolder):

    if _inputFolder != "":

        images = [
            f for f in os.listdir(_inputFolder)
            if f.lower().endswith(('.jpg', '.png'))
        ]

        # Process all images in folder
        for i in range(len(images)):
            image_filename = images[i]
            image_path = os.path.join(_inputFolder, image_filename)

            # Check if the image file exists
            if os.path.exists(image_path):
                fName = os.path.basename(image_filename)
                fName = os.path.splitext(fName)[0]
                caption = generate_caption(image_path)
                print(caption)
                MakeCaptionFile(_outputFolder, fName, caption)
            else:
                print(f"Image {image_filename} not found in {input_path}. Skipping.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Parse model argument")
    parser.add_argument('--input_file', type=str, default="", help='Caption this single image file')
    parser.add_argument('--input_folder', type=str, default="", help='Caption every image in this folder.')
    parser.add_argument('--output_folder', type=str, default="./", help='Where output file(s) are saves.')

    args = parser.parse_args()

    if args.input_folder != "":

        images = [
            f for f in os.listdir(args.input_folder)
            if f.lower().endswith(('.jpg', '.png'))
        ]

        # Process all images in folder
        for i in range(len(images)):
            image_filename = images[i]
            image_path = os.path.join(args.input_folder, image_filename)

            # Check if the image file exists
            if os.path.exists(image_path):
                fName = os.path.basename(image_filename)
                fName = os.path.splitext(fName)[0]
                caption = generate_caption(image_path)
                print(caption)
                MakeCaptionFile(args.output_folder, fName, caption)
            else:
                print(f"Image {image_filename} not found in {input_path}. Skipping.")

    else:
        if args.input_file != "":
            if os.path.exists(args.input_file):
                fName = os.path.basename(args.input_file)
                fName = os.path.splitext(fName)[0]
                caption = generate_caption(args.input_file)
                print(caption)
                MakeCaptionFile(args.output_folder, fName, caption)
            else:
                print(f"Image {args.input_file} not found. Skipping.")
