# Flask modules
from flask import Blueprint, render_template


home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/")
def home():
    return render_template("pages/home.html")
