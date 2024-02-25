from flask import Flask
from .config import Config
from .routes.compute_embedding import compute_embedding_bp


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')

    elif config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')

    else:
        app.config.from_object('app.config.Config')  # Default configuration

    app.register_blueprint(compute_embedding_bp)

    return app
