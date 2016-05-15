import datetime

from sqlalchemy import and_

from server import models, db
from server.models import Match, Bet


def add_match(tournament, home_team, away_team, time_start):
    match = models.Match(tournament=tournament, home_team=home_team, away_team=away_team, time_start=time_start)
    db.session.add(match)
    db.session.commit()


def get_nearest_matches_and_bets_by_user(user_id):
    now = datetime.datetime.utcnow()
    return db.session.query(Match, Bet) \
        .outerjoin(Bet, and_(Bet.match_id == Match.id, Bet.user_id == user_id)) \
        .filter(Match.time_start > now) \
        .all()


def get_past_matches_and_bets_by_user(user_id):
    now = datetime.datetime.utcnow()
    return db.session.query(Match, Bet) \
        .outerjoin(Bet, and_(Bet.match_id == Match.id, Bet.user_id == user_id)) \
        .filter(Match.time_start < now) \
        .all()


def add_result(away_team_score, home_team_score):
    match = models.Match(away_team_score=away_team_score, home_team_score=home_team_score)
    db.session.add(match)
    db.session.commit()
