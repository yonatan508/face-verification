import json

class ConfigManager:
    def __init__(self, config_path='app_config.json'):
        self.config_path = config_path

    def load_config(self):
        """Load the entire configuration file as a dictionary."""
        try:
            with open(self.config_path, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print("Configuration file not found, initializing with default settings.")
            return {}

    def save_config(self, config):
        """Save the provided configuration dictionary to the JSON file."""
        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        print("Configuration saved.")

    def get_class_config(self, class_id):
        """Retrieve configuration for a specific class ID."""
        config = self.load_config()
        return config.get(class_id, {})

    def set_class_config(self, class_id, directory_path=None, excel_file_path=None):
        """Set the directory and Excel file paths for a given class ID."""
        config = self.load_config()
        class_config = config.get(class_id, {})

        if directory_path is not None:
            class_config['directory_path'] = directory_path
        if excel_file_path is not None:
            class_config['excel_file_path'] = excel_file_path

        config[class_id] = class_config
        self.save_config(config)

