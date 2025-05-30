from huggingface_hub import snapshot_download
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os

# Download model to a local directory (e.g., ../hf_models)
local_dir = "../hf_models/blip-captioning"
os.makedirs(local_dir, exist_ok=True)

# Download model snapshot
model_path = snapshot_download(repo_id="Salesforce/blip-image-captioning-base", local_dir=local_dir, local_dir_use_symlinks=False)

# Load from local path
processor = BlipProcessor.from_pretrained(model_path)
model = BlipForConditionalGeneration.from_pretrained(model_path)

# Load image
image = Image.open("../siglip2_sana/fig.jpg").convert("RGB")

# Preprocess
inputs = processor(image, return_tensors="pt")

# Generate caption
with torch.no_grad():
    out = model.generate(**inputs)

# Decode
caption = processor.decode(out[0], skip_special_tokens=True)
print("Caption:", caption)

