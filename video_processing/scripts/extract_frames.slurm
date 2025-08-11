#!/bin/bash
#SBATCH --job-name=batch_frames_batch # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 1 A100 GPU
#SBATCH -N 1
#SBATCH --time=24:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=frames_batch.out # Standard output
#SBATCH --error=frames_batch.err # Standard error

set -x
cd ../

echo "Beginning transcription..."

conda run -n whisper python extract_frames.py --start "$1" --end "$2"
