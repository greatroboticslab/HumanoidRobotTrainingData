#!/bin/bash
#SBATCH --job-name=file-test     # Job name
#SBATCH --partition=a100         # Partition (queue) name
#SBATCH --gres=gpu:A100:1        # Request 1 A100 GPU
#SBATCH --nodes=1                # Number of nodes
#SBATCH --ntasks=1               # Number of tasks (usually 1 for GPU jobs)
#SBATCH --time=02:30:00          # Time limit (hh:mm:ss)
#SBATCH --output=my_job.out      # Standard output
#SBATCH --error=my_job.err       # Standard error


cd /home/imo2d/LLaVA/
# Load any necessary modules or environments
source /projects/imo2d/LLaVAGraph/bin/activate
bash scripts/v1_5/finetune_task_lora.sh
