# Video Processing

This folder is for the downloading and transcribing of videos into .txt transcripts.

## Quick Start

You should be using the Whisper environment described in the root README.

Run the command:

	sbatch batchvideos.slurm

This will download all the videos, and then transcribe them into the transcripts/ folder.

## Videos

YouTube videos are defined in videos.txt. You should paste the URLs of all the YouTube videos you wish to download, seperated by a newline.
