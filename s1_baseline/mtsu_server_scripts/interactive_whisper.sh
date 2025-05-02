srun --partition interactive --gres=gpu:2080Ti:1 --ntasks=1 --time 01:00:00 --pty bash
conda activate whisper
