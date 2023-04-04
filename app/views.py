# Flask modules
from flask import (
    render_template,
    flash,
    request,
    url_for,
    redirect,
    make_response,
    abort,
)
from flask_login import login_user, logout_user, current_user

# App modules
from app import app, db, login_manager
from app.models import User
from app.forms import RegisterForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must sign in first before you continue", category="info")
    target = request.url_rule.rule[1:]
    redirect_url = url_for("login_page") + f"?next=%2F{target}"
    return redirect(redirect_url)


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("home_page"))

    logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for("home_page"))


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        redirect_url = request.args.get("next", url_for("home_page"))
        flash(f'Success, you are signed in as "{user.username}".', category="success")
        return redirect(redirect_url)

    return render_template("auth/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))

    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(
            f'Success, your account has been created. You are now signed in as "{new_user.username}"',
            category="success",
        )
        return redirect(url_for("home_page"))

    return render_template("auth/register.html", form=form)


@app.route("/set-theme/<theme>", methods=["GET"])
def set_theme(theme: str):
    allowed_themes = ("dark", "light")
    if theme.lower() not in allowed_themes:
        return abort(400, "Invalid theme")
    response = make_response("Theme set to " + theme)
    max_age = 86400  # 1 day
    response.set_cookie("theme", value=theme, max_age=max_age)
    return response
