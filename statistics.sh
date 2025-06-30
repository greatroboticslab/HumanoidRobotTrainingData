#!/bin/bash

count=$(find ./momask_baseline/generation/batch_motions/ -mindepth 3 -maxdepth 3 -type d | wc -l)
echo "Total motions generated: $count"

count=$(find ./momask_baseline/generation/batch_motions/ -mindepth 2 -maxdepth 2 -type d | wc -l)
echo "Total motions videos processed: $count"

count=$(find ./video_processing/transcripts/ -maxdepth 1 -type f -name "*.txt" | wc -l)
echo "Total transcripts: $count"

count=$(find ./video_processing/frames/ -mindepth 3 -maxdepth 3 | wc -l)
echo "Total frames processed: $count"

count=$(find ./video_processing/frames/ -mindepth 1 -maxdepth 1 -type d | wc -l)
echo "Total frame videos processed: $count"

count=$(find ./minicpm_baseline/captions/ -mindepth 2 -maxdepth 2  | wc -l)
echo "Total captions: $count"

count=$(find ./minicpm_baseline/captions/ -mindepth 1 -maxdepth 1 -type d | wc -l)
echo "Total caption videos processed: $count"

count=$(find ./s1_baseline/output/ -mindepth 1 -maxdepth 1 -type f -name "*.json"  | wc -l)
echo "Total JSON files made for actions from videos: $count"

python statistics/count_actions.py

count=$(find ./video_processing/rawvideos/ -maxdepth 1 -type f -name "*.mp4" | wc -l)
echo "Total videos: $count"

count=$(find ./video_processing/relevant_videos/ -mindepth 1 -maxdepth 1 | wc -l)
echo "Total relevant videos: $count"

#video_processing/frames/0aN4ZuHMckU/raw_frames/
