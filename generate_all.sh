echo "Identifying videos..."
conda run -n whisper python video_processing/identify_videos.py
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
