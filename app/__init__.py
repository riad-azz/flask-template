# Flask modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Other modules
from os import path
from pathlib import Path

# Flask App
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = path.join(BASE_DIR, 'static')
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')

# App Configs
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR}/database/database.db'
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

# ---- App Managers ----
# Database manager
db = SQLAlchemy(app)
# Encryption manager
bcrypt = Bcrypt(app)
# Auth manager
login_manager = LoginManager(app)
# login_manager.login_view = 'login_page'
# login_manager.login_message = 'Please sign in to continue.'
# login_manager.login_message_category = 'info'

# App Models
from app import models

# App Routes
from app import views

