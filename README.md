# Setup CLI Tool

This CLI tool helps manage the setup and configuration of the whole-thang project modules. It provides commands for managing dependencies, VSCode tasks, and environment variables.

## Available Modules

The following modules are supported:
- `auth` - Authentication module
- `content` - Content management module
- `generation` - Generation module
- `gate` - Gateway module
- `ui` - User interface module
- `interactions` - Interactions module

## Commands

### 1. Setup Dependencies

Installs dependencies for specified modules. If no modules are specified, it will install dependencies for all modules.

```bash
python -m setup.cli dependencies [--modules MODULE1 MODULE2 ...]
```

Example:
```bash
# Install dependencies for all modules
python -m setup.cli dependencies

# Install dependencies for specific modules
python -m setup.cli dependencies --modules auth ui
```

### 2. Setup VSCode Tasks

Configures VSCode tasks and launch configurations for the specified modules. This includes setting up individual module tasks and a "Run All Modules" task.

```bash
python -m setup.cli tasks [--modules MODULE1 MODULE2 ...]
```

Example:
```bash
# Setup VSCode tasks for all modules
python -m setup.cli tasks

# Setup VSCode tasks for specific modules
python -m setup.cli tasks --modules auth ui
```

### 3. Setup Environment Variables

Configures environment variables for the specified modules using a JSON configuration file.

```bash
python -m setup.cli env --env-file PATH_TO_ENV_FILE [--modules MODULE1 MODULE2 ...]
```

Example:
```bash
# Setup environment variables for all modules
python -m setup.cli env --env-file config/env.json

# Setup environment variables for specific modules
python -m setup.cli env --env-file config/env.json --modules auth ui
```

## Environment Configuration File Format

The environment configuration file should be a JSON file with the following structure:

```json
{
  "module_name": {
    "VARIABLE_NAME": "value",
    "ANOTHER_VARIABLE": "value"
  }
}
```

Example:
```json
{
  "auth": {
    "AUTH_SECRET": "your-secret-key",
    "AUTH_PORT": "3000"
  },
  "ui": {
    "UI_PORT": "3001",
    "API_URL": "http://localhost:3000"
  }
}
```

## Notes

- The tool will automatically detect the appropriate setup type for each module (Node.js, Python, or Vite/React)
- When setting up VSCode tasks, it will create a "Run All Modules" task that can be used to start all modules simultaneously
- Environment variables are written to `.env` files in each module's directory
- If any setup step fails, the tool will report the error but continue with the remaining modules 