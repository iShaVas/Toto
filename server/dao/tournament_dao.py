from server import db, models
from server.models import Tournament


def get_all_tournaments():
    return db.session.query(Tournament.name, Tournament.name_full).order_by(Tournament.date_start).all()


def add_tournament(name, name_full, date_start, date_end):
    tournament = models.Tournament(name=name, name_full=name_full, date_start=date_start, date_end=date_end)
    db.session.add(tournament)
    db.session.commit()


def get_last_tournament():
    return Tournament.query.order_by(Tournament.date_start.desc()).first()


def get_name_full_tournament_by_name(tournament_name):
    return Tournament.query.filter(Tournament.name == tournament_name).first()
