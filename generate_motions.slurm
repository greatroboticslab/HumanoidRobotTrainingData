#!/bin/bash
#SBATCH --job-name=final_motion_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-32:4 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=12:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=logs/motion_gen.out # Standard output
#SBATCH --error=logs/motion_gen.err # Standard error

set -x
cd ${PROJECT}/PSCCode/video_processing

echo "Transcribing videos..."
conda run -n whisper python masswhisper.py > logs/masswhisper.log

cd ${PROJECT}/PSCCode/s1_baseline

echo "Generating tasks..."
conda run -n s1 python s1.py --start $1 --end $2 > logs/s1_task_generation.log

cd ${PROJECT}/PSCCode/momask_baseline

echo "Generating motions..."
conda run -n momask python generate_motions.py --start $1 --end $2 > logs/generate_momasks.log

echo "Finished generating motions."
