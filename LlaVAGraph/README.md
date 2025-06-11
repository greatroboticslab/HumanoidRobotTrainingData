# 🌋📊 LLaVAGraph

![lLLaVAGraph](https://github.com/user-attachments/assets/5db7aca4-443a-40e9-b8e6-18edd7b83b13)

`LLaVAGraph` is a multimodal agentic framework designed for classifying graphs of laser displacement data.

_Abstract:_ Pizoelectric actuator has been used extensively throughout multiple industries. The characterization of the pizoelectric actuator is important to ensure its accuracy.  This research does not only measure the displacement of the pizoelectric actuator but also  classifies different patterns of the motion using large language model. The use of the large language model has offered significant advantages by not only capable of  classification of the motion precisely but also answers the potential questions related to the pizoelectric actuator motion properties thus making it a useful tool for practical manufacturing process quality control uses.   

## Contents
- [Install](#install)
- [Finetuning](#finetuning)
- [Evaluation](#evaluation)
- [Acknowledgements](#acknowledgements)


## Install

1. Install Package
```Shell
python -m venv /projects/<username>/llava
conda create -n llava python=3.10
conda activate llava
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install --upgrade pip  # enable PEP 660 support
pip install -e .
```

2. Install additional packages for training cases
```
pip install -e ".[train]"
pip install flash-attn --no-build-isolation
```

3. Download LLaVA weights
```Shell
bash ./download-llava.bash <save-dir>
```

4. Install `deepspeed`
```Shell
pip install deepspeed
```

## Finetuning

### Dataset Format

Convert your data to a JSON file of a List of all samples. Sample metadata should contain `id` (a unique identifier), `image` (the path to the image), and `conversations` (the conversation data between human and AI).

```json
{
    "image": "SquareTrials-3-100Hz-100Hz.xlsx-17.png",
    "conversation": [
      {
        "question": "Is the line shown in the graph continuous? Describe the line.",
        "answer": "<s> This wave exhibits a non-random, yet discontinuous, pattern with sudden shifts to symmetrical peak excursions.</s>"
      },
      {
        "question": "Does the graph contain any random points?",
        "answer": "<s> The continuous line's transitions between two distinct levels are regular and predictable, demonstrating a deterministic process.</s>"
      },
      {
        "question": "Does the graph contain sharp corners?",
        "answer": "<s>  While non-random, this graph exhibits sharp corners and abrupt decreases in value.</s>"
      }
    ]
  },
```

`data/JSONData.py` contains the code to ask questions. Answers to the questions can be found [here](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%2212P1khEfULojp8iGEQU7bxZSOtv3YL3JN%22%5D,%22action%22:%22open%22,%22userId%22:%22104249159690197245312%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing).

### Modifying Training Parameters

You'll need to modify your training parameters inside `scripts/v1_5/finetune_task_lora.sh` to match your current setup.

```bash

deepspeed  <path-to-llava>/llava/train/train_mem.py \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --deepspeed <path-to-llava>/scripts/zero3.json \
    --model_name_or_path <path-you-saved-the-model> \
    --version v1 \
    --data_path <where-you-saved-the-images>/trainingData.json \
    --image_folder <where-you-saved-the-images> \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir <where-you-want-to-save-checkpoints> \
    --num_train_epochs 1 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 50000 \
    --save_total_limit 1 \
    --learning_rate 2e-4 \
    --weight_decay 0. \ 
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \ 
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \ 
    --report_to none 
```

Here is the data needed for running the trainning. Specifically, these two files are in the google drive. 

trainingData.json;
zero3.json;
the training and testing images

https://drive.google.com/file/d/1amdSPdiPv1uonQpTGUKBgJOA7TGd3wYy/view?usp=drive_link


Once you get this setup correctly, you should be able to just run:

```
sbatch slurm/training.sbatch
```

And get your final output.

## Evaluation

### Installation

Currently, evaluation requires a separate virtual environment for running LLAMA 3.2 3B (<https://huggingface.co/meta-llama/Llama-3.2-3B>). You'll need to request access to those models through Huggingface first (it took me less than an hour to get it approved, but your mileage may vary...)

```
# create a new virtual environment and activate
pip install -U "huggingface_hub[cli]"
huggingface-cli login
huggingface-cli download meta-llama/Llama-3.2-3B-Instruct --exclude "original/*" --local-dir Llama-3.2-3B-Instruct
```

<details>
<summary>MTSU cluster users</summary>
  
```
mv Llama-3.2-3B-Instruct /projects/<username>/Llama-3.2-3B-Instruct
```
  
(For whatever reason, this doesn't work well if you set `local-dir` to include the `/projects/` directory, so you'll need the extra step)
  
</details>

### Running Captioning

Look at the paths in `eval/evaluateLLaVA.sh` and change them to fit your current folder setup. Then run the training script:

```
bash scripts/evaluateLLaVA.sh
```

This will create three files in `eval/results/llava` - `randomNoise.json`, `sineWave.json`, and `squareWave.json`. This generates a description of the image:

```json
{
    "image": "SquareTrials-3-100Hz-100Hz.xlsx-17.png",
    "conversation": [
      {
        "question": "Is the line shown in the graph continuous? Describe the line.",
        "answer": "<s> This wave exhibits a non-random, yet discontinuous, pattern with sudden shifts to symmetrical peak excursions.</s>"
      },
      {
        "question": "Does the graph contain any random points?",
        "answer": "<s> The continuous line's transitions between two distinct levels are regular and predictable, demonstrating a deterministic process.</s>"
      },
      {
        "question": "Does the graph contain sharp corners?",
        "answer": "<s>  While non-random, this graph exhibits sharp corners and abrupt decreases in value.</s>"
      }
    ]
  },
```

Once these descriptions are generated, we can now run `eval/categorizeLLAMA.sh`, which takes the following information and makes a decision.

```json
{
    "conversationId": "SquareTrials-3-100Hz-100Hz.xlsx-17.png",
    "response": "Based on the information provided, I would select option C) Square wave.\n\nThe reasoning behind this decision is as follows:\n\n1. The line exhibits sharp corners and abrupt decreases in value, which aligns with the characteristics of a square wave.\n2. The line is non-random, yet discontinuous, which is also consistent with the properties of a square wave.\n3. The line's transitions between two distinct levels are regular and predictable, indicating a deterministic process, which is another characteristic of square waves.\n4. The line does not exhibit gradual transitions or easily discernible structure, which distinguishes it from a sine wave.\n\nThese characteristics collectively support the conclusion that the graph represents a square wave."
},
```

> ![NOTE]
> These scripts will only work on a GPU partition on the cluster; either use some of the `slurm` scripts or open an interactive session to run these scripts.


## LLaMA, Here is the LLama training code

https://github.com/greatroboticslab/LlaVAGraph/blob/main/eval/categorizeLLAMA.sh
https://github.com/greatroboticslab/LlaVAGraph/blob/main/eval/categorizeLLAMA.py

## Acknowledgements

- [LLaVA](https://github.com/haotian-liu/LLaVA): the base for our models
  - [Vicuna](https://github.com/lm-sys/FastChat): the codebase we built upon, and our base model Vicuna-13B that has the amazing language capabilities!
- [LLAMA 3.2 3B](https://huggingface.co/meta-llama/Llama-3.2-3B): our reasoning model

[![Code License](https://img.shields.io/badge/Code%20License-Apache_2.0-green.svg)](https://github.com/tatsu-lab/stanford_alpaca/blob/main/LICENSE)
**Usage and License Notices**: This project utilizes certain datasets and checkpoints that are subject to their respective original licenses. Users must comply with all terms and conditions of these original licenses, including but not limited to the [OpenAI Terms of Use](https://openai.com/policies/terms-of-use) for the dataset and the specific licenses for base language models for checkpoints trained using the dataset (e.g. [Llama community license](https://ai.meta.com/llama/license/) for LLaMA-2 and Vicuna-v1.5). This project does not impose any additional constraints beyond those stipulated in the original licenses. Furthermore, users are reminded to ensure that their use of the dataset and checkpoints is in compliance with all applicable laws and regulations.

