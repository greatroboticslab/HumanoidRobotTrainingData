# Output

You can generate depth frames from downloaded videos. Navigate to depth_anything_baseline/scripts/ and run either:

	bash generate_all.sh
or
	sbatch generate_depths.slurm <start> <end>

for PSC, or

	conda activate depthanything
	python Video_YTB_text.py --start <start> --end <end>

The <start> and <end> parameters determine the range of files to process. For instance, 0 and 100 will process the first 100 files. The raw frames will be saved in video_processing/output/ and the depth frames will be saved in depth_anything_baseline/output/

## Debug

The debug/ folder contains a script: grab_samples.py which can be run to grab a small amount of output data:

        python grab_samples.py --count <sample_count>

By default, the	script will try	to grab	10 folders, but	the --count argument can be used to define a custom amount.


---
title: Depth Anything V2
emoji: 🌖
colorFrom: red
colorTo: indigo
sdk: gradio
sdk_version: 4.36.0
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
