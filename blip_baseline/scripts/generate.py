#from blip3o import InferenceSession
import sys
from PIL import Image

sys.path.append('../')  # <-- change this path

from inference.inference import InferenceSession

# Initialize session
session = InferenceSession(checkpoint_dir="/path/to/checkpoint", device="cuda")

# Generate images from prompt
outputs = session.generate(
    prompt="A futuristic cityscape at sunset",
    seed=1234,
    guidance_scale=7.5,
    num_images=2
)

# Save generated images
for i, img in enumerate(outputs):
    img = Image.fromarray(img)
    img.save(f"gen_{i}.png")

