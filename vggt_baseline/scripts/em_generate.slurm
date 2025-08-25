#!/bin/bash
#SBATCH --job-name=mesh_gen # Job name
#SBATCH --partition=EM # Partition (queue) name
#SBATCH -N 1
#SBATCH --ntasks-per-node 24
#SBATCH --time=00:10:00 # Time limit (hh:mm:ss)
#SBATCH --output=mesh_gen.out # Standard output
#SBATCH --error=mesh_gen.err # Standard error

set -x

conda run -n vggt python generate.py
