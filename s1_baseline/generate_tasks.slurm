#!/bin/bash
#SBATCH --job-name=s1_task_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-32:4 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=01:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=s1_task_generation.out # Standard output
#SBATCH --error=s1_task_generation.err # Standard error

set -x

cd ../s1_baseline/
conda run -n s1 python s1.py --gpus 4
