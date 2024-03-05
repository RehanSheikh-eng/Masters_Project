from flask import Flask
from .config import Config
from .routes.compute_embedding import compute_embedding_bp
from .routes.gpt_4V import gpt_4v_bp
from flask_cors import CORS


def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)

    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')

    elif config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')

    else:
        app.config.from_object('app.config.Config')  # Default configuration

    app.register_blueprint(compute_embedding_bp)
    app.register_blueprint(gpt_4v_bp)
    
    return app
