import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_nameko import FlaskPooledClusterRpcProxy
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

environment = os.getenv('FLASK_ENV', 'development')
db = SQLAlchemy()
migrate = Migrate()
service_pool = FlaskPooledClusterRpcProxy()
api = Api()


def create_app():
    app = Flask(__name__)

    from app.config import Config, ConfigBuilder
    config = ConfigBuilder.set_app(app).set_environment(environment).get_instance()
    config.initialize()

    return app
