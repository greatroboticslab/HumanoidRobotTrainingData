#!/bin/bash

# Create target directory
MODEL_DIR="s1.1-1.5B"
mkdir -p $MODEL_DIR

# Base URL for raw files
BASE_URL="https://huggingface.co/simplescaling/s1.1-1.5B/resolve/main"

# List of files to download
FILES=(
    "config.json"
    "generation_config.json"
    "model.safetensors.index.json"
    "tokenizer.json"
    "tokenizer_config.json"
    "special_tokens_map.json"
    "vocab.json"
)

# Download each file
for file in "${FILES[@]}"; do
    echo "Downloading $file..."
    wget -q --show-progress "${BASE_URL}/${file}" -O "${MODEL_DIR}/${file}"
done

# Download model shard(s)
# NOTE: Large model shards (.safetensors) must be downloaded explicitly by name
# Adjust these names if more shards exist

SHARDS=(
    "model-00001-of-00002.safetensors"
    "model-00002-of-00002.safetensors"
)

for shard in "${SHARDS[@]}"; do
    echo "Downloading $shard..."
    wget -q --show-progress "${BASE_URL}/${shard}" -O "${MODEL_DIR}/${shard}"
done

echo "Download complete. Files saved to '${MODEL_DIR}/'"
