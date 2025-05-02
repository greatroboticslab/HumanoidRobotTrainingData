#!/bin/bash
#SBATCH --job-name=my_job # Job name
#SBATCH --partition=a100 # Partition (queue) name
#SBATCH --gres=gpu:A100:4 # Request 1 A100 GPU
#SBATCH --nodes=1 # Number of nodes
#SBATCH --ntasks=1 # Number of tasks (usually 1 for GPU jobs)
#SBATCH --time=02:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=s1_generation.out # Standard output
#SBATCH --error=s1_generation.err # Standard error

set -x

cd ..
cd s1_baseline/
conda run -n s1 python s1.py
