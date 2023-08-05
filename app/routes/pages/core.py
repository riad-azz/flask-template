# Flask modules
from flask import Blueprint, render_template

core_bp = Blueprint("core", __name__, url_prefix="/")


@core_bp.route("/")
def home_route():
    return render_template("pages/home.html")
