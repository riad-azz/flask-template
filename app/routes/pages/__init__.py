# Flask modules
from flask import Blueprint

# Blueprint modules
from .home import home_bp

pages_bp = Blueprint("pages", __name__, url_prefix="/")


pages_bp.register_blueprint(home_bp)
