import os
from abc import ABC, abstractmethod

from flask import Flask


class Config(ABC):
    SQLALCHEMY_DATABASE_URI: str
    ENV: str
    DEBUG: bool
    TESTING: bool

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    NAMEKO_AMQP_URI: str = ''

    def __init__(self, app: Flask):
        self.app = app

    def initialize(self):
        self.app.config.from_object(self)
        self._initialize_db()
        self._initialize_api()
        self._init_service_pool()

    @abstractmethod
    def _init_service_pool(self):
        ...

    def _initialize_db(self):
        from app import db, migrate
        db.init_app(self.app)
        migrate.init_app(self.app)

    def _initialize_api(self):
        from app import api
        from app.resources import url_mapping

        for resource, url in url_mapping:
            api.add_resource(resource, url)

        api.init_app(self.app)


class NonTestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    NAMEKO_AMQP_URI = os.getenv('NAMEKO_AMQP_URI', 'amqp://guest:guest@localhost')
    TESTING: bool = False

    def _init_service_pool(self):
        from app import service_pool
        service_pool.init_app(self.app)
