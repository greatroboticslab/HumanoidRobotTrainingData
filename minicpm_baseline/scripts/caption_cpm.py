import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
from transformers import AutoModelForCausalLM
import os
import argparse

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--input_file', type=str, default="", help='Caption this single image file')
parser.add_argument('--input_folder', type=str, default="", help='Caption every image in this folder.')
args = parser.parse_args()

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


# Directory containing the images
input_dir = '/home/mtsu/workspace/reshma/video_5_con_frames/Combat Robot Electronics For Beginners/'
output_dir = '/home/mtsu/workspace/reshma/video_5_con_minicpm_captions'  # Folder where the .docx files will be saved

if args.input_folder != "":

    images = [
        f for f in os.listdir(args.input_folder)
        if f.lower().endswith(('.jpg', '.png'))
    ]

    # Process all images from frame_0000 to frame_0099
    for i in range(len(images)):
        # Construct the image filename (e.g., frame_0000.jpg, frame_0001.jpg, ..., frame_0099.jpg)
        image_filename = images[i]
        image_path = os.path.join(args.input_folder, image_filename)

        # Check if the image file exists
        if os.path.exists(image_path):
            print(generate_caption(image_path))
        else:
            print(f"Image {image_filename} not found in {input_dir}. Skipping.")

