#!/bin/bash
#SBATCH --job-name=momask_example_s # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 1 A100 GPU
#SBATCH -N 1
#SBATCH --time=01:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=momask_example_s.out # Standard output
#SBATCH --error=momask_example_s.err # Standard error

set -x
cd ${PROJECT}/PSCCode/momask-codes/

pip install git+https://github.com/openai/CLIP.git

pip install --upgrade --no-cache-dir gdown

bash prepare/download_models.sh

conda run -n momask python gen_t2m.py --gpu_id 1 --ext batch_motions --text_path ../s1_baseline/output.txt

