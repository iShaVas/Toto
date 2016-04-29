import datetime

import flask_login
from server.forms import RegistrationForm, AddMatchForm
from server.match_dao import add_match, get_nearest_matches_and_bets_by_user
from server.user_dao import register_user, get_user_by_nickname
from flask import render_template, redirect, url_for
from flask_login import logout_user, current_user, login_required
from server import app, db, login_manager
from server.forms import LoginForm
from server.models import User


@login_manager.user_loader
def load_user(nickname):
    return get_user_by_nickname(nickname)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/home')
@login_required
def home():
    matches = get_nearest_matches_and_bets_by_user(current_user.id)
    return render_template('index.html', user=current_user, matches=matches, past_matches=[])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        register_user(form.first_name.data, form.last_name.data, form.email.data, form.nickname.data,
                      form.password.data)
        return render_template('register_success.html')

    return render_template('register.html', form=form)


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

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'ADMIN':
        return redirect('/')
    form = AddMatchForm()
    if form.validate_on_submit():
        date = datetime.datetime.strptime(form.time_start.data, '%Y-%m-%d %H:%M')
        date = date - datetime.timedelta(hours=form.timezone.data)
        add_match(form.tournament.data, form.home_team.data, form.away_team.data, date)
        return redirect('/admin')

    return render_template('admin.html', form=form)

