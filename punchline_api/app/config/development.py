import os

from .base import NonTestingConfig


class DevelopmentConfig(NonTestingConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    ENV = 'development'
    DEBUG = True

    def _init_service_pool(self):
        from app import service_pool
        service_pool.init_app(self.app)