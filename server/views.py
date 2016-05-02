import datetime
import json

import flask_login
import re


from server.dao.bet_dao import add_new_bet
from server.forms import RegistrationForm, AddMatchForm
from server.match_dao import add_match, get_nearest_matches_and_bets_by_user, get_past_matches_and_bets_by_user
from server.user_dao import register_user, get_user_by_nickname
from flask import render_template, redirect, url_for, jsonify
from flask_login import logout_user, current_user, login_required
from flask import request
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
    past_matches = get_past_matches_and_bets_by_user(current_user.id)
    return render_template('home.html', user=current_user, matches=matches, past_matches=past_matches)


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
    if form.is_submitted():
        if form.add_match_area.data != '':
            r = re.search('(\d\d:\d\d)\s+\"([\w\d\s]+)\"\s+-\s+\"([\w\d\s]+)\"', form.add_match_area.data)
            if r is not None:
                home_team = r.group(2)
                away_team = r.group(3)
                time = r.group(1)
                date = datetime.datetime.strptime(form.date_start.data, '%Y-%m-%d')
                time = datetime.datetime.strptime(time, '%H:%M')
                date = date.replace(hour=time.hour, minute=time.minute)
                date = date - datetime.timedelta(hours=form.timezone.data)
                add_match(form.tournament.data, home_team, away_team, date)
                return redirect('/admin')
        if form.validate():
            date = datetime.datetime.strptime(form.date_start.data, '%Y-%m-%d')
            time = datetime.datetime.strptime(form.time_start.data, '%H:%M')
            date = date.replace(hour=time.hour, minute=time.minute)
            date = date - datetime.timedelta(hours=form.timezone.data)
            add_match(form.tournament.data, form.home_team.data, form.away_team.data, date)
            return redirect('/admin')

    return render_template('admin.html', form=form)


@app.route('/save_bet', methods=['GET', 'POST'])
@login_required
def save_bet():
    data = request.form
    bet = add_new_bet(current_user.id, int(data['matchId']), int(data['homeScoreBet']), int(data['awayScoreBet']))

    return jsonify({
        'status': 'success',
        'betID': bet.id
    })




