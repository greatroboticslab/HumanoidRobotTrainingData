import cv2
import os
import re
from pytubefix import YouTube
from pytubefix.cli import on_progress
import torch
#from depth_anything_v2.dpt import DepthAnythingV2
from PIL import Image
import torchvision.transforms as T
from tqdm import tqdm
import numpy as np
import matplotlib
import argparse

parser = argparse.ArgumentParser(description="Parse model argument")
parser.add_argument('--start', type=int, default=0, help='Start from this file #')
parser.add_argument('--end', type=int, default=-1, help='Stop processing at this file, set to -1 for all files from start.')
args = parser.parse_args()

def create_folder(folder_name, depthDir):
    safe_name = re.sub(r'[\\/*?:"<>|]', '', folder_name)
    filename = "../frames/" + safe_name
    if depthDir:
        filename = "../output/" + safe_name
    os.makedirs(filename, exist_ok=True)
    return filename


def video_to_frames(video_path, output_dir, video_name, skip_frames=100):
    safe_video_name = re.sub(r'[\\/*?:"<>|]', '', video_name)
    video_name_path = os.path.join(video_path, safe_video_name)
    video_capture = cv2.VideoCapture(video_name_path)
    if not video_capture.isOpened():
        print(f"Could not open video file: {video_name_path}")
        return []

    frame_paths = []
    frame_idx = 0
    saved_idx = 0

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        if frame_idx % skip_frames == 0:
            image_path = os.path.join(output_dir, f"frame_{saved_idx:04d}.jpg")
            cv2.imwrite(image_path, frame)
            frame_paths.append(image_path)
            saved_idx += 1

        frame_idx += 1

    video_capture.release()
    return frame_paths


def read_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        return [url.strip() for url in urls]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

#    model_configs = {
#        'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
#        'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
#        'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
#        'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
#    }

#    max_depth = 80

#    encoder = "vitl"
#    model = DepthAnythingV2(**{**model_configs[encoder], 'max_depth': max_depth})
#    model.load_state_dict(torch.load(f'../checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
#    model = model.to(device).eval()

    #os.makedirs("Video_input", exist_ok=True)
    #os.makedirs("Video_output", exist_ok=True)

    _videos = [f for f in os.listdir("../relevant_videos/") if f.lower().endswith('.mp4')]

    _videos = _videos[args.start:args.end]

    if not _videos:
        print("No videos found to process.")
        return

    for video in _videos:
        if video.lower() == "q":
            break

        videoIndex = video[:-4]

        # original_video_name = download_youtube_video(url, "Video_input")
        
        if video:
            if os.path.isdir("../frames/" + os.path.splitext(os.path.basename(path))[0]):
                print("Frames alredy extracted for this video, skipping...")
            else:
                safe_folder_name = create_folder(videoIndex, False)
                frames_dir = os.path.join(safe_folder_name, "raw_frames")

                os.makedirs(frames_dir, exist_ok=True)

                print(frames_dir)
                frame_paths = video_to_frames("../relevant_videos", frames_dir, video, skip_frames=100)

    print("Processing completed.")

if __name__ == "__main__":
    main()
