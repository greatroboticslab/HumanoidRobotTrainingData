# S1

This directory stores the S1 files and scripts to extract tasks for MoMask to run.

## Quick Start

You will need to install the requirements to run the script. It is recommended to create a new environment:

	conda create -n s1

Once you have an environment, install all the requirements:

	pip install -r requirements.txt

When the requirements are finished installing, you can run the s1.py script:

	python s1.py

This script will create a list of tasks for MoMask to animate.

Alternatively, you can run a Slurm job:

	sbatch generate_tasks.slurm
