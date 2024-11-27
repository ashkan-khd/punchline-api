from flask import Flask

from .base import Config
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestConfig


class ConfigBuilder:
    __instance: "Config" = None
    __app: "Flask" = None
    __environment: "str" = None

    __environment_to_config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestConfig,
    }

    def __new__(cls, *args, **kwargs):
        raise ValueError("Cannot instantiate ConfigBuilder")

    @classmethod
    def set_app(cls, app: "Flask"):
        cls.__app = app
        return cls

    @classmethod
    def set_environment(cls, environment: str):
        cls.__environment = environment
        return cls

    @classmethod
    def get_instance(cls) -> "Config":
        try:
            app, environment = cls.__app, cls.__environment
        except AttributeError:
            raise AttributeError("app and environment must be set before getting instance")

        if not cls.__instance:
            config_class = cls.__environment_to_config.get(environment)
            assert config_class is not None, f"Invalid environment: {environment}"
            cls.__instance = config_class(app)
        return cls.__instance
