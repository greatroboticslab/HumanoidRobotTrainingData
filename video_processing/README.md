# Video Processing

This folder is for the downloading and transcribing of videos into .txt transcripts.

## Quick Start

You should be using the Whisper environment described in the root README.

Run the command:

	sbatch batchvideos.slurm

This will download all the videos, and then transcribe them into the transcripts/ folder. You can edit the .slurm file to change parameters, as currently it will download only 100 videos, 15 at a time, seperated by 5 minute intervals.

### Cookies

You may also need cookies.txt in this directory. Create the file, and use a cookies extraction extension to paste them into this file. This is due to YouTube blocking mass downloads of videos. [Here is a link describing how to get the cookies file from the yt-dlp repo.](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies)

Essenetially, we need to do this. YouTube rotates account cookies frequently on open YouTube browser tabs as a security measure. To export cookies that will remain working with yt-dlp, you will need to export cookies in such a way that they are never rotated.

One way to do this is through a private browsing/incognito window:

Open a new private browsing/incognito window and log into YouTube
Open a new tab and close the YouTube tab
Export youtube.com cookies from the browser then close the private browsing/incognito window so the session is never opened in the browser again.




## Videos

YouTube videos are defined in videos.txt. You should paste the URLs of all the YouTube videos you wish to download, seperated by a newline.

### Search Terms

You can put a list of searches into search_terms.txt, and run youtube_search.py to get the URLS of Creative Commons videos that show up when that search is used. The usage of youtube_search.py is as follows:

	youtube_search.py --input_file <name of input file, usually search_terms.txt>  --api_key <a Google API key that can use the YouTube V3 API> --max_results <how many videos the script will try to pull per search>

After search, it will generate video_s1.txt file. In this file, it includes video URLS, name, and indexes of the videos. Then, you need to run the following to download the videos.

	sbatch batchvideos.slurm

 
Example:

	python youtube_search.py --input_file search_terms.txt --api_key 1234567890REMOVEDOURAPIASIKEYTSPRIVATEINFO0987654321 --max_results 3

There is a script in the s1_baseline/ folder that generates a list of search terms, and outputs it to search_terms.txt.

### Identification

identify_videos.py can be called to generate a .csv list of videos, ids, and urls. This is useful for finding out what video belongs to what url and vice-versa.

	python identify_videos.py

### Local Download

You can use this command:

	scp username@bridges2.psc.edu:"<DIRECTORY_CONTAINING_REPO>/PSCCode/video_processing/rawvideos/*" .

To locally download all the videos into your current local directory. This may take a while, as depending on how many videos you have, there could be several gigabytes of data.
