import json

class ConfigManager:
    def __init__(self, config_path='app_config.json'):
        # Constructor that sets the path to the configuration file, defaulting to 'app_config.json'
        self.config_path = config_path

    def load_config(self):
        """Load the entire configuration file as a dictionary."""
        try:
            with open(self.config_path, 'r') as config_file:
                return json.load(config_file)  # Load and return the configuration as a dictionary
        except FileNotFoundError:
            print("Configuration file not found, initializing with default settings.")
            return {}  # Return an empty dictionary if the file does not exist

    def save_config(self, config):
        """Save the provided configuration dictionary to the JSON file."""
        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)  # Save the dictionary to a file with indentation
        print("Configuration saved.")  # Confirm that the configuration has been saved

    def get_class_config(self, class_id):
        """Retrieve configuration for a specific class ID."""
        config = self.load_config()  # Load the full configuration
        return config.get(class_id, {})  # Return the configuration for the specified class ID or an empty dict

    def set_class_config(self, class_id, directory_path=None, excel_file_path=None):
        """Set the directory and Excel file paths for a given class ID."""
        config = self.load_config()  # Load the current configuration
        class_config = config.get(class_id, {})  # Get the current class configuration or initialize a new one

        # Update the configuration with new directory and Excel file paths if provided
        if directory_path is not None:
            class_config['directory_path'] = directory_path
        if excel_file_path is not None:
            class_config['excel_file_path'] = excel_file_path

        config[class_id] = class_config  # Update the main configuration dictionary
        self.save_config(config)  # Save the updated configuration back to the file

    def delete_class_config(self, class_id):
        """Delete the configuration for a specific class ID."""
        config = self.load_config()  # Load the current configuration
        if class_id in config:
            del config[class_id]  # Remove the entry corresponding to the class ID
            self.save_config(config)  # Save the updated configuration back to the file
            print(f"Configuration for class ID {class_id} deleted.")
        else:
            print("Class ID not found in configuration.")
