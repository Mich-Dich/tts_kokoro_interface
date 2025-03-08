@echo off
REM Install and upgrade packages using uv

echo Installing and upgrading...

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found in PATH
    exit /b 1
)

REM Check if uv is installed
python -m uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing uv...
    pip install uv
)


REM Install base packages
python -m uv pip install soundfile librosa pydub || exit /b 1
python -m uv pip install ttkthemes customtkinter pillow || exit /b 1
python -m pip install pygame --upgrade

REM Uninstall and reinstall with GPU support (remove -y flag)
echo Uninstalling previous version...
python -m uv pip uninstall kokoro-onnx || echo Proceeding despite uninstall error
python -m uv pip install "kokoro-onnx[gpu]" || exit /b 1

REM Upgrade package
python -m uv pip install --upgrade kokoro-onnx || exit /b 1

echo Installation completed successfully
pause
