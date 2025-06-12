#!/bin/bash
#SBATCH --job-name=test_one # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=16:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=logs/test_one.out # Standard output
#SBATCH --error=logs/test_one.err # Standard error

echo "Submitting 1 Job..."
sbatch generate_motions.slurm 0 1
sbatch depth_anything_baseline/scripts/generate_depths.slurm 0 1
sbatch minicpm_baseline/scripts/generate_captions.slurm 0 1
