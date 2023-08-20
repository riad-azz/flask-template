# Flask modules
from flask import Flask

# Other modules
import os


def create_app(debug: bool = False):
    # Check if debug environment variable was passed
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    if FLASK_DEBUG:
        debug = FLASK_DEBUG

    # Create the Flask application instance
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    # Set current_app context
    app.app_context().push()

    if debug:
        from app.config.dev import DevConfig

        app.config.from_object(DevConfig)
    else:
        from app.config.prod import ProdConfig

        app.config.from_object(ProdConfig)

    # Uncomment to enable logger
    # from app.utils.logger import setup_flask_logger
    # setup_flask_logger()

    # Initialize extensions
    from app.extensions import db, cors, csrf, cache, bcrypt, limiter, login_manager

    db.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    # Import all models and Create database tables
    from app import models

    db.create_all()

    # Register blueprints or routes
    from app.routes import api_bp, pages_bp, auth_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    # Global Ratelimit Checker
    # this is used because auto_check is set to 'False'
    app.before_request(lambda: limiter.check())

    return app
