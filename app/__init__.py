# Flask modules
from flask import Flask

# Local modules
from app.routes import api_bp, pages_bp
from app.utils.logger import configure_logger
from app.extensions import cors, cache, limiter


def create_app(debug: bool = False):
    # Create the Flask application instance
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static",
                static_url_path="/")

    # Set current_app context
    app.app_context().push()

    if debug:
        from app.config.dev import DevConfig
        app.config.from_object(DevConfig)
    else:
        from app.config.prod import ProdConfig
        app.config.from_object(ProdConfig)

    # Set up logger
    configure_logger()

    # Initialize extensions
    cors.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Register blueprints or routes
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    return app
