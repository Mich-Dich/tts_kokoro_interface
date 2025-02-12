
# TODO:
#   add remove button to "TextBoxWidget"
#   add remove button to List blocks
#   add reorder functionality

import threading
import soundfile as sf
from kokoro_onnx import Kokoro
import os
import customtkinter as ctk
from PIL import Image
import json
import re  # Regular expressions for finding numbers in strings
import time
import pygame

is_playing = False  # Flag to track if audio is playing
kokoro = Kokoro("kokoro/kokoro-v1.0.onnx", "kokoro/voices-v1.0.bin")  # Initialize Kokoro with GPU
pygame.mixer.init()  # Initialize Pygame mixer

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

# Load icons using CTkImage
def load_icon(path, size=(20, 20)):
    image = Image.open(path)
    return ctk.CTkImage(image, size=size)

def save_data():
    data = []
    for child in scrollable_frame.winfo_children():
        if isinstance(child, ctk.CTkFrame):  # Check if it's a list container
            section_title_entry = child.winfo_children()[0]  # First child is the section name entry
            section_title = section_title_entry.get()
            widgets_frame = child.winfo_children()[1]  # Second child is the widgets frame

            texts = []
            for widget in widgets_frame.winfo_children():
                if isinstance(widget, TextBoxWidget):
                    # Get the text from the CTkTextbox
                    text = widget.text_box.get("1.0", ctk.END).strip()  # Use "1.0" to "END" for multi-line text
                    texts.append(text)

            data.append({'name': section_title, 'widgets': texts})

    with open('data.json', 'w') as f:
        json.dump(data, f)
    print("Data saved")

def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Clear existing list containers
    for child in scrollable_frame.winfo_children():
        if isinstance(child, ctk.CTkFrame):
            child.destroy()  # Remove the list container

    for section in data:
        section_title = section['name']
        texts = section['widgets']
        create_list_container(title=section_title)  # Create the list container with the section name

        # Get the widgets_frame of the newly created list container
        widgets_frame = scrollable_frame.winfo_children()[-1].winfo_children()[1]  # Last child is the new list container

        for text in texts:
            new_widget = TextBoxWidget(widgets_frame)  # Create a new TextBoxWidget
            new_widget.text_box.insert("1.0", text)  # Insert text into the CTkTextbox
            new_widget.pack(fill="x", pady=5, padx=10)  # Pack the widget to make it visible


# Custom widget class
class TextBoxWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.pack_propagate(False)  # Prevent the frame from shrinking to fit its children

        # Add a multi-line text box (CTkTextbox) to the widget
        self.text_box = ctk.CTkTextbox(self, wrap="word")  # Wrap text at word boundaries
        self.text_box.pack(pady=5, padx=10, fill="both", expand=True)  # Allow the text box to expand
        self.text_box.bind("<KeyRelease>", self.adjust_textbox_height)

        # Initial height adjustment
        self.adjust_textbox_height()

        # Create a frame to hold the buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=5, padx=10, fill="x")

        # Load icons
        self.generate_icon = load_icon("assets/generate_icon.png")
        self.play_icon = load_icon("assets/play_icon.png")
        self.remove_icon = load_icon("assets/remove_icon.png")
        self.up_icon = load_icon("assets/up_icon.png", size=(10, 10))
        self.down_icon = load_icon("assets/down_icon.png", size=(10, 10))

        # Add a "generate" button with an icon
        self.generate_button = ctk.CTkButton(
            self.button_frame, text="", image=self.generate_icon,
            width=30, height=30, corner_radius=4, command=self.on_generate
        )
        self.generate_button.pack(side="left", padx=5)

        # Add a "play" button with an icon
        self.play_button = ctk.CTkButton(
            self.button_frame, text="", image=self.play_icon,
            width=30, height=30, corner_radius=4, command=self.on_play
        )
        self.play_button.pack(side="left", padx=5)

        # Right-side buttons (remove + vertical up/down)
        right_buttons_frame = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        right_buttons_frame.pack(side="right")

        # Remove button
        self.remove_icon = load_icon("assets/remove_icon.png")
        self.remove_button = ctk.CTkButton(
            right_buttons_frame, text="", image=self.remove_icon,
            width=30, height=30, corner_radius=4, command=self.on_remove
        )
        self.remove_button.pack(side="right", padx=5)
        
        # Vertical frame for up/down buttons (half size)
        self.up_down_frame = ctk.CTkFrame(right_buttons_frame, fg_color="transparent")
        self.up_down_frame.pack(side="right", padx=5)

        # Up button
        self.up_button = ctk.CTkButton(
            self.up_down_frame, text="", image=self.up_icon,
            width=20, height=20, corner_radius=4, command=self.on_up
        )
        self.up_button.pack(side="top", pady=1)

        # Down button
        self.down_button = ctk.CTkButton(
            self.up_down_frame, text="", image=self.down_icon,
            width=20, height=20, corner_radius=4, command=self.on_down
        )
        self.down_button.pack(side="top", pady=1)

        # Defer the button visibility update until after the widget is packed
        self.after(10, self.update_button_visibility)

    # Function to adjust the height of the text box based on the number of lines
    def adjust_textbox_height(self, event=None):
        text = self.text_box.get("1.0", "end-1c")  # Get all text except the last newline
        line_count = text.count("\n") + 1  # Count newlines and add 1 for the last line
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
        section_title_entry = list_container.winfo_children()[0]
        section_title = section_title_entry.get()
        widget_index = widgets_frame.winfo_children().index(self)
        filename = f"{section_title}_{widget_index}"

        # Start a new thread for audio generation
        threading.Thread(target=self.generate_audio_thread, args=(text, filename), daemon=True).start()

    # Function to handle audio generation in a separate thread
    def generate_audio_thread(self, text, filename):
        try:
            start_time = time.time()  # Start the timer
            samples, sample_rate = kokoro.create(text, voice="af_alloy", speed=1.2, lang="en-us")  # Default voice and speed
            output_path = os.path.join("output", f"{filename}.wav")
            sf.write(output_path, samples, sample_rate)
            generation_time = time.time() - start_time
            print(f"Audio generated successfully as {filename}.wav [Time: {generation_time:.2f}s]")

        except Exception as e:
            print(f"Error generating audio: {e}")

    # Function to handle "play" button click
    def on_play(self):
        widgets_frame = self.master
        list_container = widgets_frame.master
        section_title_entry = list_container.winfo_children()[0]
        section_title = section_title_entry.get()
        widget_index = widgets_frame.winfo_children().index(self)
        filename = f"{section_title}_{widget_index}"
        output_path = os.path.join("output", f"{filename}.wav")

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
        # Remove the widget from the list
        self.destroy()
        
        # Update button visibility for all widgets in the list
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


# Create the main window
app = ctk.CTk()
app.title("CustomTkinter Window with Scrollable Lists")
app.geometry("600x600")

# Function to toggle the sidebar
sidebar_visible = False
def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar.pack_forget()  # Hide the sidebar
        toggle_button.configure(image=settings_icon)  # Show settings icon when collapsed
    else:
        sidebar.pack(side="left", fill="y")  # Show the sidebar
        toggle_button.configure(image=settings_icon)  # Keep settings icon when expanded
    sidebar_visible = not sidebar_visible

# Create a frame for the sidebar
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)

# Add a label to the sidebar
sidebar_label = ctk.CTkLabel(sidebar, text="Settings", font=("Arial", 16))
sidebar_label.pack(pady=20, padx=10)

# Add a dropdown (combobox) to the sidebar
options = [
    "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore", "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael", "am_onyx", "am_puck",
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily", "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
]
combobox = ctk.CTkComboBox(sidebar, values=options)
combobox.pack(pady=10, padx=10)
combobox.set("Select an option")  # Default text

# Add a slider to the sidebar
slider = ctk.CTkSlider(sidebar, from_=0.3, to=2.0, number_of_steps=17)
slider.pack(pady=10, padx=10)
slider.set(1.0)  # Default value

# Function to handle slider value changes
def slider_changed(value):
    print(f"Slider value: {value}")

slider.configure(command=slider_changed)

# Create a frame for the buttons at the bottom-left
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(side="left", anchor="sw", padx=5, pady=5)

# save button
save_icon = load_icon("assets/save_icon.png", size=(20, 20))
save_button = ctk.CTkButton(
    button_frame,
    text="",  # No text
    image=save_icon,  # Use the loaded settings icon
    width=30,
    height=30,
    corner_radius=4,  # Rounded corners
    command=save_data
)
save_button.pack(pady=5)

# load button
load_icon_img = load_icon("assets/load_icon.png", size=(20, 20))
load_button = ctk.CTkButton(
    button_frame,
    text="",  # No text
    image=load_icon_img,  # Use the loaded settings icon
    width=30,
    height=30,
    corner_radius=4,  # Rounded corners
    command=load_data
)
load_button.pack(pady=5)

# settings button
settings_icon = load_icon("assets/settings_icon.png", size=(20, 20))
toggle_button = ctk.CTkButton(
    button_frame,
    text="",  # No text
    image=settings_icon,  # Use the loaded settings icon
    width=30,
    height=30,
    corner_radius=4,  # Rounded corners
    command=toggle_sidebar
)
toggle_button.pack(pady=5)

# Create a scrollable frame for the lists
scrollable_frame = ctk.CTkScrollableFrame(app)
scrollable_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

def on_mouse_wheel(event):
    scrollable_frame._parent_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

app.bind_all("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview_scroll(-1, "units"))  # Up
app.bind_all("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview_scroll(1, "units"))  # Down

# Function to extract the number at the end of a string
def extract_trailing_number(s):
    match = re.search(r"\d+$", s)  # Find one or more digits at the end of the string
    if match:
        return int(match.group())  # Return the number as an integer
    return None  # Return None if no number is found


def move_list_up(list_container):
    widgets = scrollable_frame.pack_slaves()
    index = widgets.index(list_container)
    if index > 0:
        list_container.pack_forget()
        list_container.pack(fill="x", pady=10, padx=10, before=widgets[index - 1])
        update_all_list_button_visibility()

def move_list_down(list_container):
    widgets = scrollable_frame.pack_slaves()
    index = widgets.index(list_container)
    if index < len(widgets) - 1:
        list_container.pack_forget()
        list_container.pack(fill="x", pady=10, padx=10, after=widgets[index + 1])
        update_all_list_button_visibility()

def update_list_button_visibility(list_container):
    widgets = scrollable_frame.pack_slaves()
    index = widgets.index(list_container)

    # Hide "up" button if this is the topmost list
    if index == 0:
        list_container.winfo_children()[-1].winfo_children()[2].pack_forget()  # Hide up button
    else:
        list_container.winfo_children()[-1].winfo_children()[2].pack(side="left", padx=5)  # Show up button

    # Hide "down" button if this is the bottommost list
    if index == len(widgets) - 1:
        list_container.winfo_children()[-1].winfo_children()[3].pack_forget()  # Hide down button
    else:
        list_container.winfo_children()[-1].winfo_children()[3].pack(side="left", padx=5)  # Show down button

def update_all_list_button_visibility():
    for widget in scrollable_frame.pack_slaves():
        if isinstance(widget, ctk.CTkFrame):
            update_list_button_visibility(widget)

def create_list_container(title=None):
    list_containers = scrollable_frame.winfo_children()
    previous_title = "section_000"
    new_title = title
    if title == None:
        if list_containers:
            last_container = list_containers[-1]                    # Get the last list container
            entry_found = False
            for child in last_container.winfo_children():
                if isinstance(child, ctk.CTkEntry):
                    previous_title = child.get()
                    entry_found = True
                    break

            number = extract_trailing_number(previous_title)        # Extract the number at the end of the previous section name
            if number is not None:
                new_title = re.sub(r"\d+$", f"{number + 1:03d}", previous_title)
            else:
                new_title = f"{previous_title}_001"
        else:
            new_title = "section_000"

    # Create a frame for the list
    list_container = ctk.CTkFrame(scrollable_frame)
    list_container.pack(fill="x", pady=10, padx=10)

    # Add a text box for the section name
    title_entry = ctk.CTkEntry(list_container, placeholder_text="Enter section name...")
    title_entry.insert(0, new_title)  # Set the default name
    title_entry.pack(anchor="w", pady=5, padx=10, fill="x")

    # Create a frame to hold the widgets in this list
    widgets_frame = ctk.CTkFrame(list_container)
    widgets_frame.pack(fill="x", pady=5, padx=10)

    # Function to add a new TextBoxWidget to this list
    def add_widget():
        new_widget = TextBoxWidget(widgets_frame)
        new_widget.pack(fill="x", pady=5, padx=10)
        
        # Update button visibility for all widgets in the list
        for widget in widgets_frame.pack_slaves():
            if isinstance(widget, TextBoxWidget):
                widget.update_button_visibility()

    # Create a frame to hold the "Add Widget", "Remove List", and "Up/Down" buttons
    button_container = ctk.CTkFrame(list_container, fg_color="transparent")
    button_container.pack(fill="x", pady=5, padx=10)

    # Add a button to create new widgets in this list
    add_button = ctk.CTkButton(button_container, text="Add Item", command=add_widget)
    add_button.pack(side="left", padx=5)

    # Add a button to remove this list
    remove_list_icon = load_icon("assets/remove_icon.png")  # Smaller icon for the remove list button
    remove_list_button = ctk.CTkButton(
        button_container, text="", image=remove_list_icon,
        width=20, height=20, corner_radius=4, command=lambda: list_container.destroy()
    )
    remove_list_button.pack(side="left", padx=5)

    # Add "up" and "down" buttons for reordering the list
    up_icon = load_icon("assets/up_icon.png", size=(10, 10))
    down_icon = load_icon("assets/down_icon.png", size=(10, 10))

    # Up button
    up_button = ctk.CTkButton(
        button_container, text="", image=up_icon,
        width=20, height=20, corner_radius=4, command=lambda: move_list_up(list_container)
    )
    up_button.pack(side="left", padx=5)

    # Down button
    down_button = ctk.CTkButton(
        button_container, text="", image=down_icon,
        width=20, height=20, corner_radius=4, command=lambda: move_list_down(list_container)
    )
    down_button.pack(side="left", padx=5)

    # Update button visibility for the list
    update_list_button_visibility(list_container)

    # Update button visibility for all lists after creating a new one
    update_all_list_button_visibility()

# Add a button to create new lists
add_section_button = ctk.CTkButton(scrollable_frame, text="Add Section", command=create_list_container)
add_section_button.pack(pady=10)

# Run the application
app.mainloop()
