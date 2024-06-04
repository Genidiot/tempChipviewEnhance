import json
import os


class ConfigLoader:
    def __init__(self, main_config_path):
        self.main_config_path = main_config_path
        self.config = {}
        self.load_main_config()

    def load_main_config(self):
        """Loads the main configuration file."""
        with open(self.main_config_path, 'r') as file:
            self.config = json.load(file)
        self.load_external_config()

    def load_external_config(self):
        """Loads and merges the external configuration file if specified."""
        if 'externalConfig' in self.config:
            external_config_path = self.config['externalConfig']

            if os.path.exists(external_config_path):
                with open(external_config_path, 'r') as file:
                    external_config = json.load(file)
                self.merge_configs(self.config, external_config)
            else:
                print(f"External config file {external_config_path} does not exist.")

    def merge_configs(self, main, external):
        """Recursively merges the external configuration into the main configuration."""
        for key, value in external.items():
            if isinstance(value, dict) and key in main and isinstance(main[key], dict):
                self.merge_configs(main[key], value)
            else:
                main[key] = value

    def get_config(self):
        """Returns the merged configuration."""
        return self.config

    def get_value(self, key, default=None):
        """Gets a value from the configuration."""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default
