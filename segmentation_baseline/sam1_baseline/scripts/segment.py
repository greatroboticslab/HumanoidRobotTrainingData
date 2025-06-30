import os
import shutil
import glob
import random
import argparse
from PIL import Image
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

#parser = argparse.ArgumentParser(description="Parse model argument")
#parser.add_argument('--file', type=str, default="", help='Create segments this single image file')
#args = parser.parse_args()

_checkpoint = "../checkpoints/sam_vit_h_4b8939.pth"
model_type = "vit_h"

sam = sam_model_registry[model_type](checkpoint=_checkpoint)
mask_generator = SamAutomaticMaskGenerator(sam)

base_path = '../../../video_processing/frames/'


def overlay_image_alpha(base_img, overlay_img, position):
    """
    base_img: HxWx3 NumPy array (BGR)
    overlay_img: HxWx4 NumPy array (BGRA)
    position: (x, y) top-left corner where overlay is placed on base
    """
    x, y = position
    h, w = overlay_img.shape[:2]

    # Split overlay into BGR and Alpha
    overlay_bgr = overlay_img[..., :3].astype(float)
    alpha = overlay_img[..., 3:].astype(float) / (255.0 * 1.0)

    # Area to blend
    base_crop = base_img[y:y+h, x:x+w].astype(float)

    # Blend the overlay with the base
    blended = alpha * overlay_bgr + (1 - alpha) * base_crop

    # Replace the area on the base image
    base_img[y:y+h, x:x+w] = blended.astype(np.uint8)

    return base_img


# Loop through each video_id folder
for video_id in os.listdir(base_path):
    video_path = os.path.join(base_path, video_id, 'raw_frames')

    os.makedirs("output/"+video_id, exist_ok=True)

    if not os.path.isdir(video_path):
        continue  # Skip if raw_frames doesn't exist

    print(f"Processing video_id: {video_id}")
    
    # Get all .jpg files in the raw_frames folder
    jpg_files = sorted(glob.glob(os.path.join(video_path, '*.jpg')))
    
    for jpg_path in jpg_files:
        # Process each jpg file here
        print(f"  Found JPG: {jpg_path}")

        image = Image.open(jpg_path)
        image = np.array(image.convert("RGB"))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        masks = mask_generator.generate(image)

        m = masks[0]
        i = 1

        for m in masks:

            seg = m['segmentation']  # This is a 2D boolean array

            # Create an empty (H, W, 4) RGBA image
            height, width = seg.shape
            rgba = np.zeros((height, width, 4), dtype=np.uint8)

            rn = [random.randint(128, 255) for _ in range(3)]

            # Set red color and full opacity where mask is True
            rgba[seg] = [rn[0], rn[1], rn[2], 255]  # Red (R=255, G=0, B=0), Alpha=255 (opaque)

            image = overlay_image_alpha(image, rgba, (0,0))

            # Convert to image and save
            #img = Image.fromarray(rgba, mode='RGBA')
            #img.save("output/"+str(i)+".png")
            i += 1

        if image.shape[2] == 3:
            alpha_channel = np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8) * 255
            image = np.concatenate((image, alpha_channel), axis=2)

        frame_name = os.path.splitext(os.path.basename(jpg_path))[0]

        final_img = Image.fromarray(image, mode='RGBA')
        final_img.save("output/" + video_id + "/" + frame_name + ".png")
        #shutil.copy(jpg_path, "./"+frame_name+".jpg")
