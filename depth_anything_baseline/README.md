# Output

After running the Depth Anything job by doing:

	bash scripts/generate_all.sh

or by doing:

	conda activate depthanything
	python Video_YTB_text.py --start <start> --end <end>

the raw frames will be saved in ../video_processing/frames, and the depth frames will be saved in depth_anything_baseline/output/

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
