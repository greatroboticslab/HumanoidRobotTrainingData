#!/bin/bash
#SBATCH --job-name=videos_whisper_batch # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:2 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=02:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=videos_whisper_batch.out # Standard output
#SBATCH --error=videos_whisper_batch.err # Standard error

set -x
cd ${PROJECT}

cd batchdata/rawvideos/
conda run -n whisper yt-dlp -a ../videos.txt -x --audio-format mp3 -k --cookies ../cookies.txt
cd ..
conda run -n whisper python masswhisper.py
