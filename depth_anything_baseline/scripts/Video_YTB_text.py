import cv2
import os
import re
from pytubefix import YouTube
from pytubefix.cli import on_progress
import torch
from depth_anything_v2.dpt import DepthAnythingV2
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
    filename = "../../video_processing/frames/" + safe_name
    if depthDir:
        filename = "../output/" + safe_name
    os.makedirs(filename, exist_ok=True)
    return filename

def download_youtube_video(url, video_path):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        video_name = yt.title
        print(f"Downloading video: {video_name}")
        ys = yt.streams.get_highest_resolution()
        safe_filename = re.sub(r'[\\/*?:"<>|]', '', video_name) + ".mp4"
        ys.download(output_path=video_path, filename=safe_filename)
        print("Video downloaded and saved.")
        return video_name
    except Exception as e:
        print(f"Error while downloading: {e}")
        return None

def video_to_frames(video_path, output_dir, video_name, skip_frames=5):
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

def run_depth_anything_on_batch(model, image_paths, outdir, device, input_size=518, pred_only=True, grayscale=False):
    os.makedirs(outdir, exist_ok=True)
    cmap = matplotlib.colormaps.get_cmap('Spectral_r')

    for img_path in tqdm(image_paths, desc="Processing frames"):
        raw_image = cv2.imread(img_path)
        
        # Use model's built-in infer_image
        depth = model.infer_image(raw_image, input_size)
        
        depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-8) * 255.0
        depth = depth.astype(np.uint8)

        if grayscale:
            depth = np.repeat(depth[..., np.newaxis], 3, axis=-1)
        else:
            depth = (cmap(depth)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)

        if pred_only:
            output_image_path = os.path.join(outdir, os.path.splitext(os.path.basename(img_path))[0] + '.png')
            cv2.imwrite(output_image_path, depth)
        else:
            split_region = np.ones((raw_image.shape[0], 50, 3), dtype=np.uint8) * 255
            combined_result = cv2.hconcat([raw_image, split_region, depth])
            output_image_path = os.path.join(outdir, os.path.splitext(os.path.basename(img_path))[0] + '.png')
            cv2.imwrite(output_image_path, combined_result)

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

    model_configs = {
        'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
        'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
        'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
        'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
    }

    encoder = "vitl"
    model = DepthAnythingV2(**model_configs[encoder])
    model.load_state_dict(torch.load(f'../checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
    model = model.to(device).eval()

    #os.makedirs("Video_input", exist_ok=True)
    #os.makedirs("Video_output", exist_ok=True)

    _videos = [f for f in os.listdir("../../video_processing/relevant_videos/") if f.lower().endswith('.mp4')]

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
            safe_folder_name = create_folder(videoIndex, False)
            depth_folder_name = create_folder(videoIndex, True)
            frames_dir = os.path.join(safe_folder_name, "raw_frames")
            depth_dir = os.path.join(depth_folder_name, "depth_maps")

            os.makedirs(frames_dir, exist_ok=True)
            os.makedirs(depth_dir, exist_ok=True)

            print(frames_dir)
            frame_paths = video_to_frames("../../video_processing/relevant_videos", frames_dir, video, skip_frames=5)

            if frame_paths:
                print("Running DepthAnythingV2 on extracted frames...")
                run_depth_anything_on_batch(model, frame_paths, depth_dir, device)

    print("Processing completed.")

if __name__ == "__main__":
    main()
