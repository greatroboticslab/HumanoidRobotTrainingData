#!/bin/bash
#SBATCH --job-name=depth_generation # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=16:00:00 # Time limit (hh:mm:ss)
#SBATCH --output=logs/generate_all.out # Standard output
#SBATCH --error=logs/generate_all.err # Standard error

cd video_processing
echo "Identifying videos..."
conda run -n whisper python identify_videos.py
cd ..
sbatch generate_motions.slurm 0 99
sbatch generate_motions.slurm 100 199
sbatch generate_motions.slurm 200 299
sbatch generate_motions.slurm 300 399
sbatch generate_motions.slurm 400 499
sbatch generate_motions.slurm 500 599
sbatch generate_motions.slurm 600 699
sbatch generate_motions.slurm 700 799
sbatch generate_motions.slurm 800 899
sbatch generate_motions.slurm 900 999
sbatch generate_motions.slurm 1000 1099
sbatch generate_motions.slurm 1100 1199
sbatch generate_motions.slurm 1200 1299
sbatch generate_motions.slurm 1300 1399
sbatch generate_motions.slurm 1400 1499
sbatch generate_motions.slurm 1500 1599
sbatch generate_motions.slurm 1600 1699
