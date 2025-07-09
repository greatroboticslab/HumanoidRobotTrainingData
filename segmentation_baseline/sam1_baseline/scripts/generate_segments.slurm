#!/bin/bash
#SBATCH --job-name=depth_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=24:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=segm_frames.out # Standard output
#SBATCH --error=segm_frames.err # Standard error

source ${PROJECT}/miniconda3/etc/profile.d/conda.sh

set -x
cd ${PROJECT}/HumanoidRobotTrainingData/segmentation_baseline/sam1_baseline/scripts

module load cuda/12.4.0
module load gcc/13.2.1-p20240113

echo "Generating segmentations..."
conda run -n sam python segment.py --start $1 --end $2
