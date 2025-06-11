#!/bin/bash
#SBATCH --job-name=file-test     # Job name
#SBATCH --partition=a100         # Partition (queue) name
#SBATCH --gres=gpu:A100:1        # Request 1 A100 GPU
#SBATCH --nodes=1                # Number of nodes
#SBATCH --ntasks=1               # Number of tasks (usually 1 for GPU jobs)
#SBATCH --time=00:30:00          # Time limit (hh:mm:ss)
#SBATCH --output=my_job.out      # Standard output
#SBATCH --error=my_job.err       # Standard error
set -e
# Load any necessary modules or environments
echo "==> Loading modules"
module load cuda/12.4
echo "==> Creating virtual environment"
python -m venv /projects/imo2d/LLaVAGraph
echo "==> Activating conda environment"
source /projects/imo2d/LLaVAGraph/bin/activate
echo "==> Installing torch"
pip install torch
pip install --upgrade pip  # enable PEP 660 support
echo "==> Installing LLaVA"
pip install -e /home/imo2d/LLaVA/ 
echo "==> Installing LLaVA-Train"
pip install -e "/home/imo2d/LLaVA[train]"
echo "==> Installing flash-attn"
pip install flash-attn --no-build-isolation
echo "==> Installing deepspeed"
pip install deepspeed
echo "==> Done!"

