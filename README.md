# Kokoro ONNX with Custom UI

## Overview

This project extends the [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) text-to-speech (TTS) model by adding a Python-based graphical user interface (GUI). The GUI, built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), provides an intuitive way to generate and play synthesized speech.

## Features

- **GUI Interface**: A user-friendly interface for interacting with Kokoro ONNX.
- **Text Box Widgets**: Custom multi-line text inputs with automatic height adjustment.
- **Audio Generation**: Generates speech from text using Kokoro ONNX.
- **Audio Playback**: Play generated audio directly within the application.
- **Data Persistence**: Save and load text entries as JSON files.
- **Sidebar with Settings**: Toggleable sidebar with options like speed control.
- **Dynamic List Management**:
  - Add new sections and text blocks.
  - Future improvements: Remove and reorder items.

## Requirements

## Getting Started

1. Clone this repo using

```bash
git clone git@github.com:Mich-Dich/tts_kokoro_interface.git
```

2. Download the following files from [kokoro-onnx releases](https://github.com/thewh1teagle/kokoro-onnx/releases) and add them to the `tts_kokoro_interface/kokoro` dir:
- kokoro-quant-gpu.onnx
- kokoro-v1.0.fp16.onnx
- kokoro-v1.0.int8.onnx
- kokoro-v1.0.onnx

3. To set up the environment and install dependencies, run:

```bash
./setup.sh
```

## Usage

Run the application with:

```bash
./launch.sh
```

This will ensure that `kokoro-onnx` is up to date before launching the GUI.

## TODO

- add remove button to Widget
- add remove button to List blocks
- add reorder functionalityAcknowledgments

This project builds upon the [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) TTS model.

