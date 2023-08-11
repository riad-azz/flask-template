# Flask modules
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Local modules
from app.models.auth import User

bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()
