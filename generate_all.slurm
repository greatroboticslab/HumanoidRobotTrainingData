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

# Set the maximum value for s
MAX=1000  # Change this to your desired maximum value

# Starting values
s=0
f=0

while [ $f -lt $MAX ]; do
    f=$((s + 100))
    echo "Submitting Jobs: $s - $f"
    sbatch generate_motions.slurm "$s" "$f"
    cd depth_anything_baseline/scripts/
    sbatch generate_depths.slurm "$s" "$f"
    cd ../../
    cd minicpm_baseline/scripts/
    sbatch generate_captions.slurm "$s" "$f"
    cd ../../
    s=$((s + 100))
done
