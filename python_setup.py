import os
import subprocess
from typing import Dict
from .base import Setup

class PythonSetup(Setup):
    def install_dependencies(self) -> bool:
        try:
            requirements_path = os.path.join(self.module_path, "requirements.txt")
            if os.path.exists(requirements_path):
                subprocess.run(["pip", "install", "-r", requirements_path], check=True)
                return True
            return False
        except subprocess.CalledProcessError:
            return False

    @property
    def tasks_config(self) -> Dict:
        return {
            "tasks": [
                {
                    "label": f"{self.module_name}: Debug",
                    "type": "shell",
                    "command": "python",
                    "args": ["-m", "debugpy", "--listen", "5678", "--wait-for-client", "${workspaceFolder}/main.py"],
                    "group": {
                        "kind": "build",
                        "isDefault": True
                    },
                    "presentation": {
                        "reveal": "always",
                        "panel": "new"
                    },
                    "problemMatcher": []
                },
                {
                    "label": f"{self.module_name}: Run",
                    "type": "shell",
                    "command": "python",
                    "args": ["${workspaceFolder}/main.py"],
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
    def settings_config(self) -> Dict:
        return {
            "python.analysis.extraPaths": ["${workspaceFolder}"],
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            }
        }

    @property
    def launch_config(self) -> Dict:
        return {
            "configurations": [
                {
                    "name": f"{self.module_name}: Debug",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/main.py",
                    "console": "integratedTerminal",
                    "justMyCode": True
                }
            ]
        } 