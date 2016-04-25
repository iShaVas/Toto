import uuid

from flask import render_template
import flask_login

from server import app
from server.forms import RegistrationForm
from server.user_dao import register_user, get_user_by_nickname
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from server import app, db, login_manager
from server.forms import LoginForm
from server.models import User


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        register_user(form.first_name.data, form.last_name.data, form.email.data, form.nickname.data,
                      form.password.data)
        return render_template('register_success.html')

    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(nickname):
    return get_user_by_nickname(nickname)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_nickname(form.nickname.data)
        if user:
            if user.password == form.password.data:
                user = User()
                user.id = form.nickname.data
                flask_login.login_user(user)
                return redirect('/')

    return render_template('login.html',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
