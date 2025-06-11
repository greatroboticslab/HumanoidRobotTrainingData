#!/bin/bash
#SBATCH --job-name=file-test     # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-32:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=02:30:00 # Time limit (hh:mm:ss)
#SBATCH --output=my_job.out      # Standard output
#SBATCH --error=my_job.err       # Standard error


cd ../LLaVA/
# Load any necessary modules or environments
source ../bin/activate
bash scripts/v1_5/finetune_task_lora.sh
