# EVAL

> [!NOTE]
> This _should_ work without any changes; you'll probably need to change the location of your models and checkpoints.

```
-rw-r--r--. 1 imo2d domain users  528 Jan 20 21:59 categorizeLLAMA.sh
-rw-r--r--. 1 imo2d domain users  522 Jan  1 14:19 categorizePhi.sh
-rw-r--r--. 1 imo2d domain users 1129 Dec 30 11:27 eval.sh
-rw-r--r--. 1 imo2d domain users  548 Jan 20 18:20 evaluateLLaVA.sh
-rw-r--r--. 1 imo2d domain users  537 Jan 20 21:59 summarizeLLAMA.sh
```

> [!WARNING]
> These scripts are designed to called from the slurm scripts in the `slurm` folder.

I _love_ bash scripting - it really makes things easier. Most of these scripts call Python scripts over a folder of images, so they aren't _super_ complicated. ChatGPT does a great job (and helped me a lot with these!)

- <https://goalkicker.com/BashBook/BashNotesForProfessionals.pdf>

## setupDirectories.sh

- Setup the directory structure for the `results` folder.
	- Only run this once!

## cateogrizeLLAMA.sh

- Read captions from the LLaVA model and output the final answer

## categorizePhi.sh

- Same as above; don't use it though...

## eval.sh

- Older testing script; don't use for formal evaluation

## evaluateLLaVA.sh

- Caption all of our images using a finetuned LLaVA model

## summarizeLLAMA.sh

- Output final categorizations from our LLAMA model 


## experimentalAnalysis.ipynb

- Graph the results from the experiments
