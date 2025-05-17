import os
import json
from abc import ABC, abstractmethod
from typing import Dict

class Setup(ABC):
    def __init__(self, module_name: str):
        self.module_name = module_name
        # Get the directory where setup.py is located
        setup_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to reach the whole-thang directory
        self.root_dir = os.path.dirname(setup_dir)
        self.module_path = os.path.join(self.root_dir, module_name)

    @abstractmethod
    def install_dependencies(self) -> bool:
        """Install dependencies for the module."""
        pass

    @property
    @abstractmethod
    def command(self) -> str:
        """Get the command string for the module's tasks."""
        pass

    def tasks_config(self) -> Dict:
        """Get the tasks configuration for VSCode."""
        return {
            "tasks": [
                {
                    "label": f"{self.module_name}: Run",
                    "type": "shell",
                    "command": self.command,
                    "options": {
                        "cwd": "${workspaceFolder}/" + self.module_name
                    },
                    "group": "build",
                    "presentation": {
                        "reveal": "always",
                        "panel": "new"
                    },
                    "problemMatcher": []
                }
            ]
        }

    @property
    @abstractmethod
    def settings_config(self) -> Dict:
        """Get the settings configuration for VSCode."""
        pass

    @property
    @abstractmethod
    def launch_config(self) -> Dict:
        """Get the launch configuration for VSCode."""
        pass

    def setup_vscode(self) -> bool:
        """Append VSCode configuration files in the root directory."""
        vscode_dir = os.path.join(self.root_dir, ".vscode")
        os.makedirs(vscode_dir, exist_ok=True)

        try:
            # Handle tasks.json
            tasks_file = os.path.join(vscode_dir, "tasks.json")
            existing_tasks = {"version": "2.0.0", "tasks": []}
            if os.path.exists(tasks_file):
                with open(tasks_file, "r") as f:
                    existing_tasks = json.load(f)
            
            # Append new tasks
            existing_tasks["tasks"].extend(self.tasks_config()["tasks"])
            with open(tasks_file, "w") as f:
                json.dump(existing_tasks, f, indent=4)
            
            # Handle settings.json
            settings_file = os.path.join(vscode_dir, "settings.json")
            existing_settings = {}
            if os.path.exists(settings_file):
                with open(settings_file, "r") as f:
                    existing_settings = json.load(f)
            
            # Merge settings (new settings override existing ones)
            merged_settings = {**existing_settings, **self.settings_config}
            with open(settings_file, "w") as f:
                json.dump(merged_settings, f, indent=4)

            # Handle launch.json
            launch_file = os.path.join(vscode_dir, "launch.json")
            existing_launch = {"version": "0.2.0", "configurations": []}
            if os.path.exists(launch_file):
                with open(launch_file, "r") as f:
                    existing_launch = json.load(f)
            
            # Append new configurations
            existing_launch["configurations"].extend(self.launch_config["configurations"])
            with open(launch_file, "w") as f:
                json.dump(existing_launch, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error setting up VSCode: {str(e)}")
            return False

    def setup_module(self) -> bool:
        """Complete setup for the module including VSCode config and dependencies."""
        vscode_success = self.setup_vscode()
        if not vscode_success:
            return False

        return self.install_dependencies() 