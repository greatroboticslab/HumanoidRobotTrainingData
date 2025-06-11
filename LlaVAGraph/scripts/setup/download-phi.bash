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
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/added_tokens.json?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/config.json?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/configuration_phi3.py?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/generation_config.json?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/model-00001-of-00002.safetensors?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/model-00002-of-00002.safetensors?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/model.safetensors.index.json?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/special_tokens_map.json?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/tokenizer.json?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/tokenizer.model?download=true",
	"https://huggingface.co/microsoft/Phi-3.5-mini-instruct/resolve/main/tokenizer_config.json?download=true"
)

# Download each file to the specified directory
for URL in "${URLS[@]}"; do
    wget -nc -P "$DOWNLOAD_DIR" "$URL"
done
