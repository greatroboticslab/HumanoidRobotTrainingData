# Video Processing

This folder is for the downloading and transcribing of videos into .txt transcripts.

## Quick Start

You should be using the Whisper environment described in the root README.

Run the command:

	sbatch batchvideos.slurm

This will download all the videos, and then transcribe them into the transcripts/ folder.

## Videos

YouTube videos are defined in videos.txt. You should paste the URLs of all the YouTube videos you wish to download, seperated by a newline.

### Search Terms

You can put a list of searches into search_terms.txt, and run youtube_search.py to get the URLS of Creative Commons videos that show up when that search is used. The usage of youtube_search.py is as follows:

	youtube_search.py --input_file <name of input file, usually search_terms.txt>  --api_key <a Google API key that can use the YouTube V3 API> --max_results <how many videos the script will try to pull per search>

Example:

	python youtube_search.py --input_file search_terms.txt --api_key 1234567890REMOVEDOURAPIASIKEYTSPRIVATEINFO0987654321 --max_results 3

There is a script in the s1_baseline/ folder that generates a list of search terms, and outputs it to search_terms.txt.

### Local Download

You can use this command:

	scp username@bridges2.psc.edu:"<DIRECTORY_CONTAINING_REPO>/PSCCode/video_processing/rawvideos/*" .

To locally download all the videos into your current local directory. This may take a while, as depending on how many videos you have, there could be several gigabytes of data.
