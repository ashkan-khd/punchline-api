from .base import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    ENV = 'testing'
    TESTING = True
    DEBUG = True

    def _init_service_pool(self):
        pass
