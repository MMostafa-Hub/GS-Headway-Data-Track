from typing import Any
from .configurators.django_configurator import DjangoConfigurator
from .configurators.yaml_configurator import YamlConfigurator


class ConfiguratorManager:
    def __init__(self, input_type: str):
        """
        Initializes a ConfiguratorManager instance.

        Args:
            input_type (str): The type of input data source ("yaml" or "django").
        """
        self.input_type = input_type

    def create_configurator(self, **kwargs) -> Any:
        """
        Creates a configurator based on the input type and arguments.

        Args:
            **kwargs: Additional keyword arguments passed to the configurator constructor.

        Returns:
            Any: An instance of the appropriate configurator (YamlConfigurator or DjangoConfigurator).
        Raises:
            ValueError: If the input type is invalid.
        """
        if self.input_type == "yaml":
            return YamlConfigurator(**kwargs)
        elif self.input_type == "django":
            return DjangoConfigurator(**kwargs)
        else:
            raise ValueError("Invalid input type")
