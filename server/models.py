from flask_login import unicode
from server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(10), default="USER")
    token = db.Column(db.String(64), index=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament = db.Column(db.String(64), db.ForeignKey('tournament.id'), index=True)
    home_team = db.Column(db.String(64), index=True)
    away_team = db.Column(db.String(64), index=True)
    time_start = db.Column(db.DateTime, index=True)
    result = db.Column(db.Integer, index=True)
    home_team_score = db.Column(db.Integer, index=True)
    away_team_score = db.Column(db.Integer, index=True)


class Tournament(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    date_start = db.Column(db.DateTime, index=True)
    date_end = db.Column(db.DateTime, index=True)


class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), index=True)
    result = db.Column(db.Integer, index=True)
    home_team_score = db.Column(db.Integer, index=True)
    away_team_score = db.Column(db.Integer, index=True)


class UserPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), index=True)
    points = db.Column(db.Integer, index=True)