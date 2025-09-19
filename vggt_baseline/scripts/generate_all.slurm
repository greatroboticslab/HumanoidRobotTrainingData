#!/bin/bash
#SBATCH --job-name=pcloud_gen_all # Job name
#SBATCH --partition=GPU-shared # Partition (queue) name
#SBATCH --gres=gpu:v100-16:1 # Request 2 A100 GPU
#SBATCH -N 1
#SBATCH --time=00:30:00 # Time limit (hh:mm:ss)
#SBATCH --output=pcloud_gen_all.out # Standard output
#SBATCH --error=pcloud_gen_all.err # Standard error

source ../../../miniconda3/etc/profile.d/conda.sh

set -x


for dir in "../../image_processing/vggt_images"/*/; do
    if [ -d "$dir" ]; then
        conda run -n vggt python generate.py --dir "$dir"
        echo "$dir"
    fi
done
