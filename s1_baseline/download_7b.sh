#!/bin/bash

# Target directory
TARGET_DIR="s1.1-7B"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

# List of files to download
FILES=(
    "config.json"
    "generation_config.json"
    "model-00001-of-00002.safetensors"
    "model-00002-of-00002.safetensors"
    "model.safetensors.index.json"
    "special_tokens_map.json"
    "tokenizer.model"
    "tokenizer_config.json"
)

# Base URL for raw files
BASE_URL="https://huggingface.co/simplescaling/s1.1-7B/resolve/main"

# Download each file
for FILE in "${FILES[@]}"; do
    echo "Downloading $FILE..."
    curl -O "$BASE_URL/$FILE"
done

echo "Download complete. Files saved to $TARGET_DIR/"

