from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import equal_to, length, DataRequired


class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()], _name='first_name')
    last_name = StringField('Last Name', validators=[DataRequired()], _name='last_name')
    nickname = StringField('Last Name', validators=[DataRequired()], _name='nickname')
    password = PasswordField('Password', validators=[DataRequired()], _name='password')
    confirmpass = PasswordField('Confirm', validators=[equal_to('password'), length(max=255)], _name='confirmpass')
    email = StringField('Email', validators=[DataRequired()], _name='email')


class LoginForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired()], _name='nickname')
    password = PasswordField('Password', validators=[DataRequired()], _name='password')
