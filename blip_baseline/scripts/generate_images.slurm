#!/bin/bash
#SBATCH --job-name=blip_img_gen # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-32:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=24:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=img_gen.out # Standard output
#SBATCH --error=img_gen.err # Standard error

source ${PROJECT}/miniconda3/etc/profile.d/conda.sh

set -x
cd ${PROJECT}/HumanoidRobotTrainingData/blip_baseline/scripts
export HF_HOME=$PROJECT/hf_cache

echo "Generating images..."
conda run -n blip3o python generate.py --start $1 --end $2
