@echo off
REM Launch script with dependency checks

echo Checking dependencies...
python -c "import soundfile" || (
    echo Error: soundfile not installed! Run setup.bat first.
    exit /b 1
)

echo Upgrading kokoro-onnx...
python -m uv pip install --upgrade kokoro-onnx || (
    echo Upgrade failed - continuing with existing version
)

echo Starting Kokoro Audio Generator...
python main.py || (
    echo Application encountered an error
    exit /b 1
)

echo Application closed successfully
pause