import pyyaml


class ConfigManager:
    @staticmethod
    def read_yaml_config(path: str = "config.yaml"):
        """
        This function returns the yaml configuration file as a dictionary.
        """
        with open(path) as file:
            config = pyyaml.load(file, Loader=pyyaml.FullLoader)
        return config
