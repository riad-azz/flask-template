# Other modules
import re

# Flask modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, EqualTo, DataRequired, ValidationError

# App modules
from app import bcrypt
from app.models import User

# --------------     Validators     -------------- #

register_validators = {
    'username': (Length(min=2, max=30, message='Username must be between 2 to 30 characters.'), DataRequired()),
    'email': (Email(), DataRequired()),
    'password': (Length(min=8), DataRequired()),
    'confirm_password': (EqualTo('password', message='Password confirmation does not match.'), DataRequired())
}

login_validators = {
    'username': (Length(min=2, max=30, message='Username must be between 2 to 30 characters.'), DataRequired()),
    'password': (DataRequired(),),
}


# --------------     Auth Forms     -------------- #
class RegisterForm(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please try a different one.')
        if not re.match(r'^[a-z0-9]+$', username.data):
            raise ValidationError('Username can only contain lowercase characters and numbers.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'Email address already exists. Please try a different one.')

    username = StringField(label='Username', validators=register_validators['username'])
    email = StringField(label='Email address', validators=register_validators['email'])
    password = PasswordField(label='Password', validators=register_validators['password'])
    confirm_password = PasswordField(label='Confirm password', validators=register_validators['confirm_password'])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    def validate_username(self, username_input):
        username = username_input.data
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValidationError(f'Username "{username}" does not exist')

    def validate_password(self, password_input):
        password = password_input.data
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            return
        if not bcrypt.check_password_hash(user.password_hash, password):
            raise ValidationError(f'Wrong password. Please try again.')

    username = StringField(label='Username', validators=login_validators['username'])
    password = PasswordField(label='Password', validators=login_validators['password'])
    submit = SubmitField(label='Sign in')
