import customtkinter as ctk
from constants import VOICES, ICONS
import json

class SettingsSidebar:
    def __init__(self, master, audio_engine):
        self.frame = ctk.CTkFrame(master, width=200)
        self.audio_engine = audio_engine
        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self.frame, text="Settings").pack(pady=20)
        
        self.voice_combobox = ctk.CTkComboBox(self.frame, values=VOICES)
        self.voice_combobox.pack(pady=10)
        
        self.speed_slider = ctk.CTkSlider(self.frame, from_=0.5, to=2.0)
        self.speed_slider.set(1.3)
        self.speed_slider.pack(pady=10)

class ProjectSidebar:
    def __init__(self, master, project_manager):
        self.frame = ctk.CTkFrame(master, width=200)
        self.project_manager = project_manager
        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self.frame, text="Projects").pack(pady=20)
        self.projects_list = ctk.CTkScrollableFrame(self.frame)
        self.projects_list.pack(fill="both", expand=True)
        ctk.CTkButton(self.frame, text="New Project", command=self._create_project).pack(pady=10)
        ctk.CTkButton(self.frame, text="Open Project", command=self._open_project).pack(pady=10)
        self._load_recent_projects()

    def _load_recent_projects(self):
        with open(const.CONFIG_FILE, "r") as f:
            recent_projects = json.load(f)

        # Clear existing project buttons
        for widget in self.frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()

        # Add buttons for each recent project
        for project in recent_projects:
            project_button = ctk.CTkButton(self.frame, text=project["name"], command=lambda p=project: load_project(p["directory"]))
            project_button.pack(pady=5, padx=10)

        # Add a "Browse" button to load a project from a directory
        browse_button = ctk.CTkButton(self.frame, text="Browse", command=self._browse_project)
        browse_button.pack(pady=10, padx=10)
        pass

    def _create_project(self):
        print("Not implemented yet")

    def _open_project(self):
        print("Not implemented yet")

    def _browse_project(self):
        print("Not implemented yet")
