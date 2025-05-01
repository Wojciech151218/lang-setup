# Project Setup Script

This directory contains a Python script to automate the setup of a multi-repository JavaScript/Node.js project. The script will:

- Clone all required repositories into the current directory.
- Install `npm` dependencies for each repository.
- Generate VSCode configuration files (`.vscode/launch.json` and `.vscode/tasks.json`) for easy development and debugging.

## Usage

1. **Install Python 3** if you haven't already.

2. **Navigate to the directory** where you want all repositories and the `.vscode` folder to be created.

3. **Run the setup script:**

   ```sh
   python setup/main.py
   ```

   - If you need to provide an SSH passphrase for private repositories, use:
     ```sh
     python setup/main.py --ssh-passphrase YOUR_PASSPHRASE
     ```

## What the Script Does

- **Clones Repositories:**  
  The script clones the following repositories into the current directory:
  - `auth`: [auth-service](https://github.com/Wojciech151218/auth-service.git)
  - `content`: [content-service](https://github.com/Wojciech151218/content-service.git)
  - `gateway`: [lang-gateway](https://github.com/Wojciech151218/lang-gateway.git)
  - `frontend`: [ui-prototype-2](https://github.com/Wojciech151218/ui-prototype-2.git)

- **Installs Dependencies:**  
  Runs `npm install` in each cloned repository.

- **Creates VSCode Configurations:**  
  - `.vscode/launch.json` with launch configurations for each service and a "Run All Services" option.
  - `.vscode/tasks.json` with tasks to start each service in development mode (`npm run dev`) and a task to start all services at once.

## Notes

- The script is cross-platform and will work on Windows, macOS, and Linux.
- If a repository already exists, it will not be cloned again.
- If a repository is missing, its dependencies will not be installed and no launch configuration will be created for it.

## Customization

- To add or remove repositories, edit the `self.repos` dictionary in `setup/main.py`.
- To change the npm command (e.g., use `npm run start` instead of `npm run dev`), modify the `command` in the `create_vscode_config` method.

---

**Happy coding!**
