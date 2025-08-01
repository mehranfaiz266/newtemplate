from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class CredentialForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    api_key = StringField('API Key', validators=[DataRequired()])
    api_secret = StringField('API Secret', validators=[DataRequired()])
    submit = SubmitField('Save')
