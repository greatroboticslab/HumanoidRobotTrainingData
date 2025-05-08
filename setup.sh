echo "Installing Whisper dependencies..."
cd ${PROJECT}/PSCCode/video_processing
conda create -n whisper python=3.12
conda activate whisper
python3 -m pip install -U "yt-dlp[default]"
pip install -U openai-whisper
conda install conda-forge::ffmpeg

echo "Installing S1 dependencies..."
cd ${PROJECT}/PSCCode/s1_baseline
conda create -n s1
pip install -r requirements.txt
git clone https://huggingface.co/simplescaling/s1.1-7B

echo "Installing MoMask dependencies..."
cd ${PROJECT}/PSCCode/momask_baseline
conda env create -f environment.yml
conda activate momask
pip install git+https://github.com/openai/CLIP.git
bash prepare/download_models.sh	

echo "Finished setting up."
