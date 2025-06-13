#!/bin/bash
#SBATCH --job-name=depth_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=16:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=depth_frames.out # Standard output
#SBATCH --error=depth_frames.err # Standard error

source ../../../miniconda3/etc/profile.d/conda.sh

set -x
cd ../../depth_anything_baseline/scripts

echo "Generating depth frames..."
conda run -n depthanything python Video_YTB_text.py --start $1 --end $2 > ../logs/depth_frames.log
