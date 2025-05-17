import subprocess
from typing import Dict
from .base import Setup

class NodeSetup(Setup):
    def install_dependencies(self) -> bool:
        try:
            subprocess.run("npm install", cwd=self.module_path, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @property
    def tasks_config(self) -> Dict:
        return {
            "tasks": [
                {
                    "label": f"{self.module_name}: Debug",
                    "type": "shell",
                    "command": "npm",
                    "args": ["run", "dev"],
                    "cwd": "${workspaceFolder}/" + self.module_name,
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
                    "command": "npm",
                    "args": ["run", "start"],
                    "cwd": "${workspaceFolder}/" + self.module_name,
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
            "typescript.tsdk": "node_modules/typescript/lib"
        }

    @property
    def launch_config(self) -> Dict:
        return {
            "configurations": [
                {
                    "type": "node",
                    "request": "launch",
                    "name": f"{self.module_name}: Debug",
                    "skipFiles": ["<node_internals>/**"],
                    "runtimeExecutable": "npm",
                    "runtimeArgs": ["run", "dev"],
                    "cwd": "${workspaceFolder}/" + self.module_name,
                    "console": "integratedTerminal",
                    "outFiles": ["${workspaceFolder}/" + self.module_name + "/**/*.js"]
                }
            ]
        } 