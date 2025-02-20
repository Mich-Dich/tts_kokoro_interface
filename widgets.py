from kokoro_onnx import Kokoro
from PIL import Image
import threading
import soundfile as sf
import os
import customtkinter as ctk
import time
import pygame
import constants as const
import project_manager

kokoro = Kokoro("kokoro/kokoro-v1.0.onnx", "kokoro/voices-v1.0.bin")  # Initialize Kokoro with GPU
pygame.mixer.init()  # Initialize Pygame mixer

class TextBoxWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.pack_propagate(False)                                                      # Prevent the frame from shrinking to fit its children

        self.text_box = ctk.CTkTextbox(self, wrap="word")                               # Add a multi-line text box (CTkTextbox) to the widget
        self.text_box.pack(pady=5, padx=10, fill="both", expand=True)                   # Allow the text box to expand
        self.text_box.bind("<KeyRelease>", self.adjust_textbox_height)

        self.adjust_textbox_height()                                                    # Initial height adjustment

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")                  # Create a frame to hold the buttons
        self.button_frame.pack(pady=5, padx=10, fill="x")

        self.generate_button = ctk.CTkButton(self.button_frame, text="", image=const.ICONS['generate'], width=30, height=30, corner_radius=4, command=self.on_generate)
        self.generate_button.pack(side="left", padx=5)

        self.play_button = ctk.CTkButton(self.button_frame, text="", image=const.ICONS['play'], width=30, height=30, corner_radius=4, command=self.on_play)
        self.play_button.pack(side="left", padx=5)

        right_buttons_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")   # Right-side buttons (remove + vertical up/down)
        right_buttons_frame.pack(side="right")

        self.remove_button = ctk.CTkButton(right_buttons_frame, text="", image=const.ICONS['remove'], width=30, height=30, corner_radius=4, command=self.on_remove)
        self.remove_button.pack(side="right", padx=5)
        
        self.up_down_frame = ctk.CTkFrame(right_buttons_frame, fg_color="transparent")  # Vertical frame for up/down buttons (half size)
        self.up_down_frame.pack(side="right", padx=5)

        self.up_button = ctk.CTkButton(self.up_down_frame, text="", image=const.ICONS['up'], width=20, height=20, corner_radius=4, command=self.on_up)
        self.up_button.pack(side="top", pady=1)

        self.down_button = ctk.CTkButton(self.up_down_frame, text="", image=const.ICONS['down'], width=20, height=20, corner_radius=4, command=self.on_down)
        self.down_button.pack(side="top", pady=1)

        self.after(10, self.update_button_visibility)                                   # Defer the button visibility update until after the widget is packed

    def adjust_textbox_height(self, event=None):                                        # Function to adjust the height of the text box based on the number of lines
        text = self.text_box.get("1.0", "end-1c")                                       # Get all text except the last newline
        line_count = text.count("\n") + 1                                               # Count newlines and add 1 for the last line
        min_height = 1
        max_height = 10
        new_height = min(max(line_count, min_height), max_height)
        self.text_box.configure(height=new_height)
        self.configure(height=new_height * 20 + 100)  # Adjust this formula as needed

    # Function to handle "generate" button click
    def on_generate(self):
        text = self.text_box.get("1.0", ctk.END).strip()  # Use "1.0" to "END" to get all text
        widgets_frame = self.master
        list_container = widgets_frame.master
        title_frame = list_container.winfo_children()[0]
        title_entry = title_frame.winfo_children()[0]
        section_title = title_entry.get()
        widget_index = widgets_frame.winfo_children().index(self)
        filename = f"{section_title}_{widget_index}"
        print(f"current_project_directory: {project_manager.current_project_directory}")

        # Start a new thread for audio generation
        threading.Thread(target=self.generate_audio_thread, args=(text, filename), daemon=True).start()

    # Function to handle audio generation in a separate thread
    def generate_audio_thread(self, text, filename):
        try:
            start_time = time.time()  # Start the timer
            samples, sample_rate = kokoro.create(text, voice="af_alloy", speed=1.2, lang="en-us")  # Default voice and speed

            # Use the current project directory to save the .wav file
            if project_manager.current_project_directory:
                output_path = os.path.join(project_manager.current_project_directory, const.OUTPUT_DIR, f"{filename}.wav")
            else:
                output_path = os.path.join(const.OUTPUT_DIR, f"{filename}.wav")

            sf.write(output_path, samples, sample_rate)
            generation_time = time.time() - start_time
            print(f"Audio generated successfully as {filename}.wav [Time: {generation_time:.2f}s]")

        except Exception as e:
            print(f"Error generating audio: {e}")

    # Function to handle "play" button click
    def on_play(self):
        widgets_frame = self.master
        list_container = widgets_frame.master
        title_frame = list_container.winfo_children()[0]
        title_entry = title_frame.winfo_children()[0]
        section_title = title_entry.get()
        widget_index = widgets_frame.winfo_children().index(self)
        filename = f"{section_title}_{widget_index}"

        # Use the current project directory to locate the .wav file
        if project_manager.current_project_directory:
            output_path = os.path.join(project_manager.current_project_directory, f"{filename}.wav")
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

    # Function to handle "remove" button click
    def on_remove(self):
        self.destroy()
        widgets_frame = self.master
        for widget in widgets_frame.pack_slaves():
            if isinstance(widget, TextBoxWidget):
                widget.update_button_visibility()

    def on_up(self):
        widgets_frame = self.master
        widgets = widgets_frame.pack_slaves()
        index = widgets.index(self)
        if index > 0:
            self.pack_forget()
            self.pack(fill="x", pady=5, padx=10, before=widgets[index - 1])
            self.update_button_visibility()
            widgets[index - 1].update_button_visibility()

    def on_down(self):
        widgets_frame = self.master
        widgets = widgets_frame.pack_slaves()
        index = widgets.index(self)
        if index < len(widgets) - 1:
            self.pack_forget()
            self.pack(fill="x", pady=5, padx=10, after=widgets[index + 1])
            self.update_button_visibility()
            widgets[index + 1].update_button_visibility()

    # Function to update button visibility based on position
    def update_button_visibility(self):
        widgets_frame = self.master
        widgets = widgets_frame.pack_slaves()
        index = widgets.index(self)

        # Hide "up" button if this is the topmost widget
        if index == 0:
            self.up_button.pack_forget()
        else:
            self.up_button.pack(side="top", pady=1)

        # Hide "down" button if this is the bottommost widget
        if index == len(widgets) - 1:
            self.down_button.pack_forget()
        else:
            self.down_button.pack(side="top", pady=1)