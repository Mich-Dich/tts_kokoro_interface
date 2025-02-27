import soundfile as sf
from kokoro_onnx import Kokoro
import pygame
import threading
import time
import os
import project_manager
import constants as const

pygame.mixer.init()
kokoro = Kokoro(str(const.MODEL_PATH), str(const.VOICES_PATH))


selected_voice = const.DEFAULT_VOICE
voice_speed = 1.2

# Function to update the selected voice
def update_selected_voice(choice):
    global selected_voice
    selected_voice = choice
    print(f"Selected voice updated to: {selected_voice}")  # Debug statement

def update_voice_speed(choice):
    global voice_speed
    voice_speed = choice
    print(f"Voice speed updated to: {voice_speed}")  # Debug statement

def play_audio(filename):
    if project_manager.current_project_directory:
        output_path = os.path.join(project_manager.current_project_directory, const.OUTPUT_DIR, f"{filename}.wav")
    else:
        output_path = os.path.join(const.OUTPUT_DIR, f"{filename}.wav")

    # Play the audio if it exists
    if os.path.exists(output_path):
        try:
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            print(f"Playing audio [{filename}.wav]")
        except Exception as e:
            print(f"Error playing audio: {e}")
    else:
        print(f"Audio file not found: {filename}.wav")

def generate_in_thread(text, filename, voice, speed, lang, callback):
    def thread_target():
        try:
            duration = generate_audio(text, filename, voice, speed, lang)
            callback(True, filename, duration)
        except Exception as e:
            callback(False, str(e))
    threading.Thread(target=thread_target, daemon=True).start()

def generate_audio(text, filename):
    print(f"current_project_directory: {project_manager.current_project_directory}")
    threading.Thread(target=generate_audio_thread, args=(text, filename), daemon=True).start()       # Start a new thread for audio generation with the selected voice and speed

# Function to handle audio generation in a separate thread
def generate_audio_thread(text, filename):
    try:
        print(f"generate_audio_thread: {selected_voice}, {voice_speed}")
        start_time = time.time()  # Start the timer
        samples, sample_rate = kokoro.create(text, voice=selected_voice, speed=voice_speed, lang="en-us")  # Use the selected voice and speed

        # Use the current project directory to save the .wav file
        if project_manager.current_project_directory:
            output_path = os.path.join(project_manager.current_project_directory, const.OUTPUT_DIR, f"{filename}.wav")
        else:
            output_path = os.path.join(const.OUTPUT_DIR, f"{filename}.wav")

        sf.write(output_path, samples, sample_rate)
        generation_time = time.time() - start_time
        print(f"Audio generated successfully as {output_path}/{filename}.wav [Time: {generation_time:.2f}s]")

    except Exception as e:
        print(f"Error generating audio: {e}")
