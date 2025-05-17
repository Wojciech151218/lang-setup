import argparse
from . import NodeSetup, PythonSetup, ViteReactSetup
import os

def setup_dependencies(args):
    """Setup dependencies for specified modules."""
    modules = args.modules if args.modules else ["auth", "content", "generation", "gate", "ui"]
    setups = []
    
    for module in modules:
        if module in ["auth", "content", "gate"]:
            setups.append(NodeSetup(module))
        elif module == "generation":
            setups.append(PythonSetup(module))
        elif module == "ui":
            setups.append(ViteReactSetup(module))
    
    for setup in setups:
        print(f"Setting up dependencies for {setup.module_name}...")
        if setup.install_dependencies():
            print(f"✓ Successfully installed dependencies for {setup.module_name}")
        else:
            print(f"✗ Failed to install dependencies for {setup.module_name}")

def clear_vscode_config():
    """Clear all VSCode configuration files."""
    vscode_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".vscode")
    if os.path.exists(vscode_dir):
        for file in ["tasks.json", "settings.json", "launch.json"]:
            file_path = os.path.join(vscode_dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)

def setup_tasks():
    """Setup VSCode tasks and launch configurations for all modules."""
    modules = ["auth", "content", "generation", "gate", "ui"]
    setups = []
    
    # Clear existing VSCode configuration
    clear_vscode_config()
    
    for module in modules:
        if module in ["auth", "content", "gate"]:
            setups.append(NodeSetup(module))
        elif module == "generation":
            setups.append(PythonSetup(module))
        elif module == "ui":
            setups.append(ViteReactSetup(module))
    
    for setup in setups:
        print(f"Setting up VSCode configuration for {setup.module_name}...")
        if setup.setup_vscode():
            print(f"✓ Successfully configured VSCode for {setup.module_name}")
        else:
            print(f"✗ Failed to configure VSCode for {setup.module_name}")

def main():
    parser = argparse.ArgumentParser(description="Setup tool for the whole-thang project")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup dependencies command
    deps_parser = subparsers.add_parser("dependencies", help="Setup dependencies for modules")
    deps_parser.add_argument(
        "--modules",
        nargs="+",
        choices=["auth", "content", "generation", "gate", "ui"],
        help="Specific modules to setup (default: all modules)"
    )

    # Setup tasks command
    tasks_parser = subparsers.add_parser("tasks", help="Setup VSCode tasks and launch configurations")
    tasks_parser.add_argument(
        "--modules",
        nargs="+",
        choices=["auth", "content", "generation", "gate", "ui"],
        help="Specific modules to setup (default: all modules)"
    )

    args = parser.parse_args()

    if args.command == "dependencies":
        setup_dependencies(args)
    elif args.command == "tasks":
        setup_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 