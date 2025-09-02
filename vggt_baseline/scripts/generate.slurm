#!/bin/bash
#SBATCH --job-name=pcloud_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=00:30:00 # Time limit (hh:mm:ss)
#SBATCH --output=pcloud_generation.out # Standard output
#SBATCH --error=pcloud_generation.err # Standard error

source ../../../miniconda3/etc/profile.d/conda.sh

set -x

conda run -n vggt python generate.py --dir ../../image_processing/strawberryfield/
