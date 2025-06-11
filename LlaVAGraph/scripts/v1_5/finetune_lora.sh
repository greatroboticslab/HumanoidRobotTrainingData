#!/bin/bash

deepspeed llava/train/train_mem.py \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --model_name_or_path ../llava-v1.6-vicuna-7b/ \
    --deepspeed ./scripts/zero3.json \
    --version v1 \
    --data_path ../formattedData.json \
    --image_folder ../drive/MyDrive/CroppedImages \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --bf16 True \
    --output_dir ./checkpoints/llava-v1.5-13b-lora \
    --num_train_epochs 1 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --save_steps 50000 \
    --save_total_limit 1 \
    --weight_decay 0. \
    --warmup_ratio 0.1 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --learning_rate 2e-4
    --report_to wandb
