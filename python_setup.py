import os
import subprocess
from typing import Dict
from .base import Setup

class PythonSetup(Setup):
    def __init__(self, module_name: str):
        super().__init__(module_name)
        self.venv_path = os.path.join(self.module_path, "venv")
        self.venv_python = os.path.join(self.venv_path, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(self.venv_path, "bin", "python")
        self.venv_pip = os.path.join(self.venv_path, "Scripts", "pip.exe") if os.name == 'nt' else os.path.join(self.venv_path, "bin", "pip")

    def install_dependencies(self) -> bool:
        try:
            # Create virtual environment if it doesn't exist
            if not os.path.exists(self.venv_path):
                print(f"Creating virtual environment for {self.module_name}...")
                subprocess.run(["python", "-m", "venv", self.venv_path], check=True)

            # Install requirements if they exist
            requirements_path = os.path.join(self.module_path, "requirements.txt")
            if os.path.exists(requirements_path):
                print(f"Installing dependencies for {self.module_name}...")
                subprocess.run([self.venv_pip, "install", "-r", requirements_path], check=True)
                return True
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error during setup: {str(e)}")
            return False

    def get_venv_activate_command(self) -> str:
        if os.name == 'nt':  # Windows
            return f"& {os.path.join(self.venv_path, 'Scripts', 'activate.ps1')}"
        else:  # Unix/Linux/MacOS
            return f"source {os.path.join(self.venv_path, 'bin', 'activate')}"

    @property
    def command(self) -> str:
        venv_activate = self.get_venv_activate_command()
        workspace_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
        if os.name == 'nt':
            return f"{venv_activate}; python $env:WORKSPACE_FOLDER/{self.module_name}/src/main.py"
        return f"{venv_activate} && python {workspace_path}/{self.module_name}/src/main.py"

    @property
    def settings_config(self) -> Dict:
        venv_activate = self.get_venv_activate_command()
        return {
            "python.analysis.extraPaths": [
                "${workspaceFolder}/" + self.module_name,
                "${workspaceFolder}/" + self.module_name + "/src"
            ],
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            },
            "python.autoComplete.extraPaths": [
                "${workspaceFolder}/" + self.module_name,
                "${workspaceFolder}/" + self.module_name + "/src"
            ],
            "python.defaultInterpreterPath": self.venv_python
        }

    @property
    def launch_config(self) -> Dict:
        return {
            "configurations": [
                {
                    "name": f"{self.module_name}: Debug",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/" + self.module_name + "/src/main.py",
                    "console": "integratedTerminal",
                    "justMyCode": True,
                    "cwd": "${workspaceFolder}/" + self.module_name,
                    "python": self.venv_python,
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}/" + self.module_name
                    }
                }
            ]
        } 