import os
import json

class EnvironmentSetup:
    def __init__(self, env_config_path):
        self.env_config_path = env_config_path
        self.env_config = self._load_env_config()

    def _load_env_config(self):
        """Load environment configuration from JSON file."""
        try:
            with open(self.env_config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error reading environment configuration file: {str(e)}")

    def setup_module_env(self, module_name):
        """Setup environment variables for a specific module."""
        if module_name not in self.env_config:
            raise Exception(f"No environment configuration found for module {module_name}")

        module_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), module_name)
        env_path = os.path.join(module_dir, ".env")

        try:
            with open(env_path, "w") as f:
                for key, value in self.env_config[module_name].items():
                    f.write(f"{key}={value}\n")
            return True
        except Exception as e:
            raise Exception(f"Error setting up environment for {module_name}: {str(e)}")

    def setup_all_modules(self, modules=None):
        """Setup environment variables for specified modules or all modules if none specified."""
        modules = modules if modules else list(self.env_config.keys())
        results = []

        for module in modules:
            try:
                self.setup_module_env(module)
                results.append((module, True, None))
            except Exception as e:
                results.append((module, False, str(e)))

        return results 