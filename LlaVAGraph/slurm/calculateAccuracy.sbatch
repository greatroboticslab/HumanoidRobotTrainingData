#!/bin/bash
#SBATCH --job-name=file-test     # Job name
#SBATCH --partition=a100         # Partition (queue) name
#SBATCH --gres=gpu:A100:1        # Request 1 A100 GPU
#SBATCH --nodes=1                # Number of nodes
#SBATCH --ntasks=1               # Number of tasks (usually 1 for GPU jobs)
#SBATCH --time=01:00:00          # Time limit (hh:mm:ss)
#SBATCH --output=/home/imo2d/LLaVA/slurm/summarizeLLAMA.out      # Standard output
#SBATCH --error=/home/imo2d/LLaVA/slurm/summarizeLLAMA.err       # Standard error

cd /home/imo2d/LLaVA/eval
# Load any necessary modules or environments
source /projects/imo2d/phi-eval/bin/activate
bash summarizeLLAMA.sh

