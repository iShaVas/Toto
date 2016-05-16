import datetime
import re

import flask_login
from flask import render_template, redirect, url_for, jsonify
from flask import request
from flask_login import logout_user, current_user, login_required
from server.dao.match_dao import add_match, get_nearest_matches_and_bets_by_user, get_past_matches_and_bets_by_user, \
    add_result

from server import app, login_manager
from server.dao.bet_dao import add_new_bet, get_points_of_users_by_tournament
from server.dao.user_dao import register_user, get_user_by_nickname
from server.dao.match_dao import get_past_matches_and_bets_by_tournament
from server.forms import LoginForm
from server.forms import RegistrationForm, AddMatchForm
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
            strings = form.add_match_area.data.split("\r\n")
            for string in strings:
                if string != '':
                    r = re.search('(\d\d:\d\d)\s+\"?([\w\d\s]+)\"?\s+-\s+\"?([\w\d\s]+)\"?', string)
                    if r is not None:
                        home_team = r.group(2)
                        away_team = r.group(3)
                        time = r.group(1)
                        date = datetime.datetime.strptime(form.date_start.data, '%Y-%m-%d')
                        time = datetime.datetime.strptime(time, '%H:%M')
                        date = date.replace(hour=time.hour, minute=time.minute)
                        date = date - datetime.timedelta(hours=form.timezone.data)
                        add_match(form.tournament.data, home_team, away_team, date)
                    else:
                        print("Cannot add this string: " + string)
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
    return add_new_bet(current_user.id, int(data['matchId']), int(data['homeScoreBet']), int(data['awayScoreBet']))


@app.route('/save_match_result', methods=['GET', 'POST'])
def save_match_result():
    if current_user.role != 'ADMIN':
        return None
    data = request.form
    return add_result(int(data['matchId']), int(data['homeScoreBet']), int(data['awayScoreBet']))


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    users, match_user_bet = get_past_matches_and_bets_by_tournament("UCL2015")

    rating_table = get_points_of_users_by_tournament("UCL2015")

    return render_template('statistics.html', users=users, matches_data=match_user_bet, rating_table=rating_table)


@app.route('/addresult', methods=['GET', 'POST'])
def add_result_match():
    matches = get_nearest_matches_and_bets_by_user(current_user.id)
    past_matches = get_past_matches_and_bets_by_user(current_user.id)
    return render_template('addresult.html', user=current_user, matches=matches, past_matches=past_matches)


@app.route('/settings')
def settings():
    login = get_user_by_nickname(current_user.id)
    return render_template('settings.html', user=current_user)
