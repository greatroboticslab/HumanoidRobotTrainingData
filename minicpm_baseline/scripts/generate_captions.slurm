#!/bin/bash
#SBATCH --job-name=caption_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-32:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=24:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=../logs/generate_captions.out # Standard output
#SBATCH --error=../logs/generate_captions.err # Standard error

source ${PROJECT}/miniconda3/etc/profile.d/conda.sh

set -x
cd ${PROJECT}/HumanoidRobotTrainingData/minicpm_baseline/scripts

echo "Generating captions..."
conda run -n minicpm python generate_captions.py --start $1 --end $2
