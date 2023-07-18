from flask import Flask

from app.routes import api_bp, pages_bp
from app.extensions import cors, limiter
from app.config import DevConfig, ProdConfig


def create_app(debug: bool = False):
    # Create the Flask application instance
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static",
                static_url_path="/")

    if debug:
        app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)

    # Initialize extensions
    cors.init_app(app)
    limiter.init_app(app)

    # Register blueprints or routes
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    # Set current_app context
    app.app_context().push()

    return app
