#!/bin/bash
# Thanks ChatGPT!

# Check if a directory is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <download-directory>"
    exit 1
fi

# Create the directory if it doesn't exist
DOWNLOAD_DIR="$1"
mkdir -p "$DOWNLOAD_DIR"

# Define the list of files to download
URLS=(
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/generation_config.json"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/config.json"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/.gitattributes"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/model-00001-of-00003.safetensors"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/model-00002-of-00003.safetensors"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/model-00003-of-00003.safetensors"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/model.safetensors.index.json"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/special_tokens_map.json"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/training_args.bin"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/trainer_state.json"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/tokenizer_config.json"
    "https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/resolve/main/tokenizer.model"
)

# Download each file to the specified directory
for URL in "${URLS[@]}"; do
    wget -nc -P "$DOWNLOAD_DIR" "$URL"
done
