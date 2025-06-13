#!/bin/bash
#SBATCH --job-name=s1_searchterm_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-32:4 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=2-00:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=s1_searchterm_generation.out # Standard output
#SBATCH --error=s1_searchterm_generation.err # Standard error

set -x

cd ../s1_baseline/
conda run -n s1 python generate_search_terms.py --gpus 4 --searches 50000
