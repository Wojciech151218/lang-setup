import os
import subprocess
import json
from pathlib import Path
import shutil
import argparse
import platform
import sys

class ProjectSetup:
    def __init__(self, ssh_passphrase=None):
        self.base_dir = Path.cwd()
        self.repos = {
            "auth": "git@github.com:Wojciech151218/auth-service.git",
            "content": "git@github.com:Wojciech151218/content-service.git",
            "gateway": "git@github.com:Wojciech151218/lang-gateway.git",
            "frontend": "git@github.com:Wojciech151218/ui-prototype-2.git",
        }
        self.vscode_dir = self.base_dir / ".vscode"
        self.launch_json = self.vscode_dir / "launch.json"
        self.ssh_passphrase = ssh_passphrase
        self.is_windows = platform.system().lower() == 'windows'

    def clone_repositories(self):
        """Clone all repositories defined in self.repos"""
        for name, url in self.repos.items():
            repo_dir = self.base_dir / name
            if repo_dir.exists():
                print(f"Repository {name} already exists. Skipping...")
                continue
            
            print(f"Cloning {name}...")
            
            # Set up SSH environment with passphrase if provided
            env = os.environ.copy()
            if self.ssh_passphrase:
                env["SSH_PASSPHRASE"] = self.ssh_passphrase
            
            try:
                # Use absolute path for git clone
                subprocess.run(["git", "clone", url, str(repo_dir.absolute())], 
                             env=env, 
                             check=True,
                             shell=self.is_windows)  # Use shell=True on Windows
            except subprocess.CalledProcessError as e:
                print(f"Error cloning {name}: {str(e)}")
                if not self.ssh_passphrase:
                    print("Note: SSH passphrase might be required for private repositories")
                continue

    def install_dependencies(self):
        """Run npm install for each repository"""
        for name in self.repos.keys():
            repo_dir = self.base_dir / name
            if not repo_dir.exists():
                print(f"Repository {name} not found. Skipping npm install...")
                continue

            print(f"Installing dependencies for {name}...")
            try:
                # Use absolute path for npm install
                subprocess.run(["npm", "install"], 
                             cwd=str(repo_dir.absolute()),
                             shell=self.is_windows,  # Use shell=True on Windows
                             check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error installing dependencies for {name}: {str(e)}")
                continue

    def create_vscode_config(self):
        """Create VSCode launch configurations"""
        if not self.vscode_dir.exists():
            self.vscode_dir.mkdir(parents=True, exist_ok=True)

        # Create individual launch configurations for each service
        configurations = []
        for name in self.repos.keys():
            repo_dir = self.base_dir / name
            if not repo_dir.exists():
                continue

            # Use platform-agnostic path separators in VSCode config
            relative_path = str(Path(name))
            
            # Add individual service configuration
            configurations.append({
                "name": f"Run {name}",
                "type": "node",
                "request": "launch",
                "cwd": f"${{workspaceFolder}}/{relative_path}",
                "runtimeExecutable": "npm",
                "runtimeArgs": ["run", "start"],
                "console": "integratedTerminal"
            })

        # Add configuration to run all services
        configurations.append({
            "name": "Run All Services",
            "type": "node",
            "request": "launch",
            "cwd": "${workspaceFolder}",
            "runtimeExecutable": "npm",
            "runtimeArgs": ["run", "start"],
            "console": "integratedTerminal",
            "preLaunchTask": "start-all-services"
        })

        # Create tasks.json for running all services
        tasks = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "start-all-services",
                    "dependsOn": [f"start-{name}" for name in self.repos.keys()],
                    "group": {
                        "kind": "build",
                        "isDefault": True
                    }
                }
            ]
        }

        # Add individual service tasks
        for name in self.repos.keys():
            relative_path = str(Path(name))
            tasks["tasks"].append({
                "label": f"start-{name}",
                "type": "shell",
                "command": "npm run dev",
                "options": {
                    "cwd": f"${{workspaceFolder}}/{relative_path}"
                },
                "isBackground": True
            })

        # Write launch.json
        launch_config = {
            "version": "0.2.0",
            "configurations": configurations
        }
        
        with open(self.launch_json, 'w', encoding='utf-8') as f:
            json.dump(launch_config, f, indent=4)

        # Write tasks.json
        tasks_json = self.vscode_dir / "tasks.json"
        with open(tasks_json, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4)

    def setup_project(self):
        """Run the complete setup process"""
        try:
            print("Starting project setup...")
            print(f"Base directory: {self.base_dir.absolute()}")
            self.clone_repositories()
            self.install_dependencies()
            self.create_vscode_config()
            print("Project setup completed successfully!")
        except Exception as e:
            print(f"Error during setup: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup project with VSCode configurations')
    parser.add_argument('--ssh-passphrase', 
                       help='SSH passphrase for private repositories',
                       required=False)
    args = parser.parse_args()
    
    setup = ProjectSetup(ssh_passphrase=args.ssh_passphrase)
    setup.setup_project()
