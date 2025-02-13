#!/bin/bash

# Upgrade kokoro-onnx using uv
echo "Installing and upgrading..."

uv pip install ttkthemes customtkinter pillow
uv pip uninstall kokoro-onnx
uv pip install kokoro-onnx[gpu]
uv pip install --upgrade kokoro-onnx