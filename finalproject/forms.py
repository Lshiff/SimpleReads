from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, InputRequired, Length, Email, EqualTo

from .database_manager import DatabaseManager

class RegisterForm(FlaskForm):
    display_name = StringField('Display Name', validators = [InputRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators = [InputRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [
        InputRequired(),
        EqualTo('password', message="Passwords must match")
    ])

    def validate_username(self, username):
        if DatabaseManager.username_exists(username.data):
            raise ValidationError("Username already exists")

    def validate_email(self, email):
        if DatabaseManager.email_exists(email.data):
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
