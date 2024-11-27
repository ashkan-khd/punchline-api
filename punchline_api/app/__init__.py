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

    # Config from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['NAMEKO_AMQP_URI'] = os.getenv('NAMEKO_AMQP_URI', 'amqp://guest:guest@localhost')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    if environment != 'testing':
        service_pool.init_app(app)

    # Initialize Flask-RESTful
    init_api(app)

    return app


def init_api(flask_app):
    from .resources import url_mapping

    for resource, url in url_mapping:
        api.add_resource(resource, url)

    api.init_app(flask_app)
