# project_manager.py
import json
import os
from pathlib import Path
from constants import CONFIG_DIR, OUTPUT_DIR
import constants as const

current_project_directory = None
recent_projects = None


def create_project_directory(directory):                                        # Create the necessary directories for a new project
    os.makedirs(directory, exist_ok=True)
    os.makedirs(os.path.join(directory, OUTPUT_DIR), exist_ok=True)

def save_project_data(data):                                                    # Save project data to the specified directory
    if not current_project_directory:
        print("No project directory selected.")
        return

    with open(os.path.join(current_project_directory, 'tts_kokoro.json'), 'w') as f:
        json.dump(data, f)

    print("Data saved")
    update_recent_projects(current_project_directory, os.path.basename(current_project_directory))

def load_project_data(directory):                                               # Load project data from the specified directory
    if not directory:
        print("No project directory selected.")
        return None

    with open(os.path.join(directory, 'tts_kokoro.json'), 'r') as f:
        data = json.load(f)
    return data

def update_recent_projects(directory, name):                                    # Update the list of recent projects
    recent_projects_file = const.CONFIG_FILE
    if not recent_projects_file.exists():
        with open(recent_projects_file, 'w') as f:
            json.dump([], f)

    with open(recent_projects_file, 'r') as f:
        recent_projects = json.load(f)

    # Check if the project is already in the list
    for project in recent_projects:
        if project["directory"] == directory:
            return

    recent_projects.append({"name": name, "directory": directory})
    if len(recent_projects) > 5:
        recent_projects = recent_projects[-5:]

    with open(recent_projects_file, 'w') as f:
        json.dump(recent_projects, f)

def get_recent_projects():                                                      # Get the list of recent projects
    recent_projects_file = const.CONFIG_FILE
    if not recent_projects_file.exists():
        return []

    with open(recent_projects_file, 'r') as f:
        return json.load(f)

def load_project(directory):                                                    # Load a project from the specified directory
    global current_project_directory
    current_project_directory = directory
    return load_project_data(directory)

def load_project_by_name(project_name):                                         # Load a project by its name from the list of recent projects
    for project in recent_projects:
        if project["name"] == project_name:
            return load_project(project["directory"])
    print(f"Project '{project_name}' not found in recent projects.")
    return None

def browse_project():                                                           # Browse for a project directory
    import customtkinter as ctk
    directory = ctk.filedialog.askdirectory()
    if directory:
        load_project(directory)
        return directory
    return None

def create_new_project():
    import customtkinter as ctk
    from tkinter import messagebox
    directory = ctk.filedialog.askdirectory(title="Select Directory for New Project")
    if not directory:
        return None
    
    global current_project_directory
    current_project_directory = directory  # <-- ADD THIS

    # Create project directory and data.json
    os.makedirs(directory, exist_ok=True)
    data_path = os.path.join(directory, 'tts_kokoro.json')
    if not os.path.exists(data_path):
        with open(data_path, 'w') as f:
            json.dump([], f)
    
    # Update recent projects
    project_name = os.path.basename(directory)
    update_recent_projects(directory, project_name)
    
    # Refresh recent projects list
    global recent_projects
    recent_projects = get_recent_projects()
    
    messagebox.showinfo("Success", f"Project created: {project_name}")
    return directory

recent_projects = get_recent_projects()