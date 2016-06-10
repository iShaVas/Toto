from server import db
from server.models import Tournament


def get_all_tournaments():
    return db.session.query(Tournament.name, Tournament.name).all()