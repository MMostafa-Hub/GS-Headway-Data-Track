from typing import Any
from .configurators.django_configurator import DjangoConfigurator
from .configurators.yaml_configurator import YamlConfigurator


class ConfiguratorManager:
    def __init__(self, input_type: str):
        self.input_type = input_type

    def create_configurator(self, **kwargs) -> Any:
        if self.input_type == "yaml":
            return YamlConfigurator(**kwargs)
        elif self.input_type == "django":
            return DjangoConfigurator(**kwargs)
        else:
            raise ValueError("Invalid input type")
