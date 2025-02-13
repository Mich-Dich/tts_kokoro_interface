import os
from pathlib import Path
import customtkinter as ctk
from PIL import Image

# Paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
CONFIG_DIR = BASE_DIR / "config"
MODEL_PATH = BASE_DIR / "kokoro" / "kokoro-v1.0.onnx"
VOICES_PATH = BASE_DIR / "kokoro" / "voices-v1.0.bin"

OUTPUT_DIR = "output"

# Voices
VOICES = [
    "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore", "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael", "am_onyx", "am_puck",
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
]

# Defaults
DEFAULT_VOICE = "af_alloy"
DEFAULT_SPEED = 1.2
DEFAULT_LANG = "en-us"
DEFAULT_PROJECT_NAME = "Untitled Project"

# Icons
def create_icon(path, size=(20, 20)):
    return ctk.CTkImage(Image.open(path), size=size)

ICONS = {
    'up':       create_icon(ASSETS_DIR / "up_icon.png", (10, 10)),
    'down':     create_icon(ASSETS_DIR / "down_icon.png", (10, 10)),
    'collapse': create_icon(ASSETS_DIR / "collapse_icon.png"),
    'generate': create_icon(ASSETS_DIR / "generate_icon.png"),
    'play':     create_icon(ASSETS_DIR / "play_icon.png"),
    'pause':    create_icon(ASSETS_DIR / "pause_icon.png"),
    'stop':     create_icon(ASSETS_DIR / "stop_icon.png"),
    'remove':   create_icon(ASSETS_DIR / "remove_icon.png"),
    'save':     create_icon(ASSETS_DIR / "save_icon.png", (20, 20)),
    'load':     create_icon(ASSETS_DIR / "load_icon.png", (20, 20)),
    'settings': create_icon(ASSETS_DIR / "settings_icon.png", (20, 20)),
}

# Project config
RECENT_PROJECTS_FILE = CONFIG_DIR / "recent_projects.json"
