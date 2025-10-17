#!/bin/bash
#SBATCH --job-name=momask_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 1 A100 GPU
#SBATCH -N 1
#SBATCH --time=24:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=momask_generation.out # Standard output
#SBATCH --error=momask_generation.err # Standard error

set -x
cd ../

pip install git+https://github.com/openai/CLIP.git

pip install --upgrade --no-cache-dir gdown

conda run -n momask python generate_motions.py --start "$1" --end "$2"
