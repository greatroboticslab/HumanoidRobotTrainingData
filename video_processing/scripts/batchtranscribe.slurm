#!/bin/bash
#SBATCH --job-name=videos_whisper_batch # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 1 A100 GPU
#SBATCH -N 1
#SBATCH --time=24:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=transcribe_batch.out # Standard output
#SBATCH --error=transcribe_batch.err # Standard error

# CONFIGURATION
ENV_NAME="whisper"
FILES=(../output/video_downloading/videos.txt ../output/video_downloading/videos_s1_${1}*.txt)   # Add paths to your .txt files here
BATCH_SIZE=15
SLEEP_BETWEEN_BATCHES=300                   # Seconds between batches
MAX_DOWNLOADS=100                      # <-- Set your max video downloads here

set -x
cd ${PROJECT}/HumanoidRobotTrainingData
cd video_processing

echo "Beginning transcription..."

conda run -n whisper python masswhisper.py --start "$1" --end "$2"
