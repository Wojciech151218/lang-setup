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
    def command(self) -> str:
        return "npm run start"

    @property
    def settings_config(self) -> Dict:
        return {
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            },
            "typescript.tsdk": "node_modules/typescript/lib",
            "debug.javascript.autoAttachFilter": "smart",
            "debug.javascript.terminalOptions": {
                "skipFiles": ["<node_internals>/**"]
            }
        }

    @property
    def launch_config(self) -> Dict:
        return {
            "version": "0.2.0",
            "configurations": [
                {
                    "cwd": "${workspaceFolder}/" + self.module_name,
                    "type": "node",
                    "request": "launch",
                    "name": f"{self.module_name}: Debug",
                    "skipFiles": [
                        "<node_internals>/**"
                    ],
                    "program": "${workspaceFolder}/" + self.module_name + "/src/index.ts",
                    "sourceMaps": True,
                    "resolveSourceMapLocations": [
                        "${workspaceFolder}/**",
                        "!**/node_modules/**"
                    ],
                    "console": "integratedTerminal",
                    "internalConsoleOptions": "neverOpen",
                    "restart": True,
                    "autoAttachChildProcesses": True,
                    "runtimeExecutable": "node",
                    "runtimeArgs": [
                        "--nolazy",
                        "-r",
                        "ts-node/register"
                    ],
                    "env": {
                        "TS_NODE_PROJECT": "${workspaceFolder}/"+self.module_name+"/tsconfig.json"
                    }
                }
            ]
        } 