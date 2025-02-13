import soundfile as sf
from kokoro_onnx import Kokoro
import pygame
import threading
import time
from constants import MODEL_PATH, VOICES_PATH, OUTPUT_DIR

pygame.mixer.init()
kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))

class AudioHandler:
    @staticmethod
    def generate_audio(text, filename, voice, speed, lang):
        try:
            start_time = time.time()
            samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang=lang)
            output_path = OUTPUT_DIR / f"{filename}.wav"
            sf.write(output_path, samples, sample_rate)
            return time.time() - start_time
        except Exception as e:
            raise e

    @staticmethod
    def play_audio(filename):
        output_path = OUTPUT_DIR / f"{filename}.wav"
        if output_path.exists():
            try:
                pygame.mixer.music.load(str(output_path))
                pygame.mixer.music.play()
                return True
            except Exception as e:
                raise e
        return False

    @staticmethod
    def generate_in_thread(text, filename, voice, speed, lang, callback):
        def thread_target():
            try:
                duration = AudioHandler.generate_audio(text, filename, voice, speed, lang)
                callback(True, filename, duration)
            except Exception as e:
                callback(False, str(e))
        threading.Thread(target=thread_target, daemon=True).start()
