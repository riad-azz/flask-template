# Flask modules
from flask import Flask
from flask_limiter import ExemptionScope

# Local modules
from app.routes import api_bp, pages_bp
from app.extensions import cors, cache, limiter
from app.config import DevConfig, ProdConfig


def create_app(debug: bool = False):
    # Create the Flask application instance
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static",
                static_url_path="/")

    # Set current_app context
    app.app_context().push()

    if debug:
        app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)

    # Initialize extensions
    cors.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Exempt pages from the ratelimit
    limiter.exempt(pages_bp,
                   flags=ExemptionScope.DEFAULT |
                         ExemptionScope.APPLICATION |
                         ExemptionScope.DESCENDENTS)

    # Register blueprints or routes
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    return app
