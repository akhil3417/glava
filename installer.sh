#!/bin/bash

# Create virtualenv and activate
virtualenv -p python3.10 .env && . .env/bin/activate

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is not active."
    exit 1
fi

# install python packages
pip install -r requirements.txt

# add custom roles to shellgpt roles
cp ./scripts/jarvis.json ~/.config/shell_gpt/roles/

# Create directories
mkdir -p ./extensions/vosk
mkdir -p ./extensions/piper
mkdir -p ./extensions/piper/models

# Download Vosk model
if [ ! -f ./extensions/vosk/vosk-model-small-en-us-0.15.zip ]; then
    wget -O ./extensions/vosk/vosk-model-small-en-us-0.15.zip "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    unzip ./extensions/vosk/vosk-model-small-en-us-0.15.zip -d ./extensions/vosk
fi

# Download Piper
if [ ! -f ./extensions/piper/piper_linux_$(uname -m).tar.gz ]; then
    wget -O ./extensions/piper/piper_linux_$(uname -m).tar.gz "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_$(uname -m).tar.gz"
    tar -xvf ./extensions/piper/piper_linux_$(uname -m).tar.gz -C ./extensions/piper
fi

# Download Piper models
if [ ! -f ./extensions/piper/models/en_US-hfc_female-medium.onnx.json ]; then
    wget -O ./extensions/piper/models/en_US-hfc_female-medium.onnx.json "https://huggingface.co/rhasspy/piper-voices/raw/main/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx.json"
fi

if [ ! -f ./extensions/piper/models/en_US-hfc_female-medium.onnx ]; then
    wget -O ./extensions/piper/models/en_US-hfc_female-medium.onnx "https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx"
fi

# Make necessary files executable
chmod +x ./extensions/piper/piper
