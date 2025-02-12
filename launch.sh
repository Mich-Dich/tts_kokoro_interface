#!/bin/bash

# Upgrade kokoro-onnx using uv
echo "Upgrading kokoro-onnx..."
uv pip install --upgrade kokoro-onnx

# Check if the upgrade was successful
if [ $? -eq 0 ]; then
    echo "kokoro-onnx upgraded successfully."
else
    echo "Failed to upgrade kokoro-onnx. Please check your setup."
    exit 1
fi

# Run the ui.py script using uv
echo "Starting the Kokoro Audio Generator..."
uv run ui.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    echo "Kokoro Audio Generator closed successfully."
else
    echo "Kokoro Audio Generator encountered an error."
    exit 1
fi
