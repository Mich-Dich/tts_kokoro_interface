# project_manager.py
import json
import os
from pathlib import Path
from constants import CONFIG_DIR

class ProjectManager:
    def __init__(self):
        self.current_project = None
        self.recent_projects_file = CONFIG_DIR / "recent_projects.json"
        self._init_files()

    def _init_files(self):
        CONFIG_DIR.mkdir(exist_ok=True)
        if not self.recent_projects_file.exists():
            self.recent_projects_file.write_text('[]')

    def create_project(self, directory):
        (Path(directory) / 'data.json').write_text('[]')
        self.current_project = directory
        self._update_recent_projects(directory)

    def load_project(self, directory):
        self.current_project = directory
        self._update_recent_projects(directory)
        return self._load_data()

    def _load_data(self):
        with open(Path(self.current_project) / 'data.json') as f:
            return json.load(f)

    def save_project(self, data):
        if not self.current_project:
            return False
            
        with open(Path(self.current_project) / 'data.json', 'w') as f:
            json.dump(data, f)
        self._update_recent_projects(self.current_project)
        return True

    def _update_recent_projects(self, directory):
        try:
            projects = json.loads(self.recent_projects_file.read_text())
        except:
            projects = []

        # Remove duplicates
        projects = [p for p in projects if p['directory'] != str(directory)]
        
        projects.insert(0, {
            'name': Path(directory).name,
            'directory': str(directory)
        })
        
        self.recent_projects_file.write_text(json.dumps(projects[:5]))
