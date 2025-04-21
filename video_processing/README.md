# Video Processing

This folder is for the downloading and transcribing of videos into .txt transcripts.

## Quick Start

You should be using the Whisper environment described in the root README.

Run the command:

	sbatch batchvideos.slurm

This will download all the videos, and then transcribe them into the transcripts/ folder.

## Videos

YouTube videos are defined in videos.txt. You should paste the URLs of all the YouTube videos you wish to download, seperated by a newline.

### Local Download

You can use this command:

	scp username@bridges2.psc.edu:"<DIRECTORY_CONTAINING_REPO>/PSCCode/video_processing/rawvideos/*" .

To locally download all the videos into your current local directory. This may take a while, as depending on how many videos you have, there could be several gigabytes of data.
