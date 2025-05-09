#!/bin/bash
#SBATCH --job-name=final_motion_generation # Job name
#SBATCH --partition=interactive # Partition (queue) name
#SBATCH --gres=gpu:2080Ti:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=02:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=motion_gen.out # Standard output
#SBATCH --error=motion_gen.err # Standard error

set -x
cd video_processing

echo "Identifying videos..."
conda run -n whisper python identify_videos.py

echo "Transcribing videos..."
conda run -n whisper python masswhisper.py

cd ../s1_baseline

echo "Generating tasks..."
conda run -n s1 python s1.py --model s1.1-1.5B --gpus 1 --tokens 4096

cd ../momask_baseline

echo "Generating motions..."
conda run -n momask python generate_motions.py

echo "Finished generating motions."
