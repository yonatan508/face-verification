import json

class ConfigManager:
    def __init__(self, config_path='app_config.json'):
        # Constructor that sets the path to the configuration file, defaulting to 'app_config.json'
        self.config_path = config_path

    def load_config(self):
        """Load the entire configuration file as a dictionary.
        Attempts to open and read the JSON configuration file. If the file is not found,
        it returns an empty dictionary and prints a message indicating initialization with default settings."""
        try:
            with open(self.config_path, 'r') as config_file:
                return json.load(config_file)  # Load and return the configuration as a dictionary
        except FileNotFoundError:
            print("Configuration file not found, initializing with default settings.")
            return {}  # Return an empty dictionary if the file does not exist

    def save_config(self, config):
        """Save the provided configuration dictionary to the JSON file.
        Writes the configuration dictionary to the specified JSON file with proper formatting (indentation)."""
        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)  # Save the dictionary to a file with indentation
        print("Configuration saved.")  # Confirm that the configuration has been saved

    def get_class_config(self, class_id):
        """Retrieve configuration for a specific class ID.
        Loads the entire configuration and returns the part relevant to the specified class ID.
        Returns an empty dictionary if the class ID is not found."""
        config = self.load_config()  # Load the full configuration
        return config.get(class_id, {})  # Return the configuration for the specified class ID or an empty dict

    def set_class_config(self, class_id, directory_path=None, excel_file_path=None):
        """Set the directory and Excel file paths for a given class ID.
        Modifies the configuration for a specific class, allowing updates to directory paths and Excel file paths."""
        config = self.load_config()  # Load the current configuration
        class_config = config.get(class_id, {})  # Get the current class configuration or initialize a new one

        # Update the configuration with new directory and Excel file paths if provided
        if directory_path is not None:
            class_config['directory_path'] = directory_path
        if excel_file_path is not None:
            class_config['excel_file_path'] = excel_file_path

        config[class_id] = class_config  # Update the main configuration dictionary
        self.save_config(config)  # Save the updated configuration back to the file
