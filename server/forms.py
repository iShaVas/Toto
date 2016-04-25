from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import equal_to, length, DataRequired


class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    nickname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpass = PasswordField('Confirm', validators=[equal_to('password'), length(max=255)])
    email = StringField('Email', validators=[DataRequired()])


class LoginForm(Form):
    nickname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
