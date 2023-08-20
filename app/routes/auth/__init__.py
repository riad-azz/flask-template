# Flask modules
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from flask_login import login_user, logout_user

# Other modules
import logging

# Local modules
from app.models.auth import User
from app.extensions import db, bcrypt, limiter
from app.forms.auth import LoginForm, RegistrationForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("30/minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("pages.core.home_route"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember_me)
            flash(f"Logged in successfully as {user.name}", "success")
            return redirect(url_for("pages.core.home_route"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("30/minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("pages.core.home_route"))

    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.generate_password_hash(password)

        # Add user to database
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Login user
        login_user(new_user)

        flash(
            f"Account created successfully! You are now logged in as {new_user.name}.",
            "success",
        )
        return redirect(url_for("pages.core.home_route"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
