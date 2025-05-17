import os
import subprocess
from typing import Dict
from .base import Setup

class ViteReactSetup(Setup):
    def install_dependencies(self) -> bool:
        try:
            package_json_path = os.path.join(self.module_path, "package.json")
            if not os.path.exists(package_json_path):
                subprocess.run("npm create vite@latest . -- --template react-ts", cwd=self.module_path, shell=True, check=True)
            
            subprocess.run("npm install", cwd=self.module_path, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @property
    def tasks_config(self) -> Dict:
        return {
            "tasks": [
                {
                    "label": f"{self.module_name}: Dev Server",
                    "type": "shell",
                    "command": "npm",
                    "args": ["run", "dev"],
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
                    "label": f"{self.module_name}: Build",
                    "type": "shell",
                    "command": "npm",
                    "args": ["run", "build"],
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
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            },
            "typescript.tsdk": "node_modules/typescript/lib",
            "typescript.enablePromptUseWorkspaceTsdk": True,
            "editor.defaultFormatter": "esbenp.prettier-vscode",
            "[typescript]": {
                "editor.defaultFormatter": "esbenp.prettier-vscode"
            },
            "[typescriptreact]": {
                "editor.defaultFormatter": "esbenp.prettier-vscode"
            }
        }

    @property
    def launch_config(self) -> Dict:
        return {
            "configurations": [
                {
                    "type": "chrome",
                    "request": "launch",
                    "name": f"{self.module_name}: Debug",
                    "url": "http://localhost:5173",
                    "webRoot": "${workspaceFolder}",
                    "sourceMapPathOverrides": {
                        "webpack:///src/*": "${webRoot}/src/*"
                    }
                }
            ]
        } 