# PSC Server Code

This repo contains the code we execute on the PSC server to obtain animation data for humanoid robot farming.

## Quick Start

### Setup

### For Whisper
You should create a conda environment called whisper. This is optional, but the SLURM batch jobs provided use this environment.

	conda create -n whisper python=3.12
	conda activate whisper

You will need yt-dlp:

	python3 -m pip install -U "yt-dlp[default]"

You will also need whisper, which will convert audio to transcripts:

	pip install -U openai-whisper

Finally, you will need PyTube:

	pip install pytube

There is a text file called videos.txt in the video_processing folder. Paste YouTube links separated by a newline into this text folder for videos you wish to download.


### For S1 Scallinglaw


### Running the Job

Once you have the dependencies installed, you can run batchvideos.slurm in the video_processing folder:

	sbatch batchvideos.slurm

This will submit a job that will download the YouTube videos (stored in rawvideos), extract the audio, and then generate text transcripts of the videos (stored in transcripts).

## Workflow

START -> batch video download (video_id.mp3) -> Whisper transcription -> S1 Analysis (tasks/reject) -> MoMask Motion Generation -> END
S1 Analysis -> Generate a text file of urls that were not rejected for being irrelevant.
