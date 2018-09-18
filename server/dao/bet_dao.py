import datetime

from flask import jsonify
from sqlalchemy import func

from server import db
from server.dao.match_dao import get_match_by_id
from server.models import Bet, User, Match


def add_new_bet(user_id, match_id, home_score, away_score):
    now = datetime.datetime.utcnow()
    match = get_match_by_id(match_id)

    if match.time_start < now:
        return jsonify({
            'status': 'failed',
            'reason': 'Этот матч уже начался',
            'betID': None
        })

    bet = Bet.query.filter(Bet.user_id == user_id, Bet.match_id == match_id).first()

    if bet:
        bet.home_team_score = home_score
        bet.away_team_score = away_score
    else:
        bet = Bet(user_id, match_id, home_score, away_score, 3) # edit here
        db.session.add(bet)
        db.session.flush()

    db.session.commit()

    return jsonify({
        'status': 'success',
        'betID': bet.id
    })


def get_points_of_users_by_tournament(tournament_id):
    return db.session.query(User, func.count(Bet.total_points).label('count'), func.sum(Bet.points).label("points"), func.sum(Bet.total_points).label("total_points"), Match) \
        .outerjoin(Bet, Bet.user_id == User.id) \
        .outerjoin(Match, Bet.match_id == Match.id) \
        .filter(Match.tournament == tournament_id) \
        .filter(Bet.points is not None) \
        .group_by(Bet.user_id) \
        .order_by(func.sum(Bet.total_points).desc(), func.count(Bet.total_points)) \
        .all()


def get_points_of_users_by_tournament_last_day(tournament_id):
    last_match_time = db.session.query(Match.time_start).order_by(Match.time_start.desc()).filter(Match.time_start < datetime.datetime.now()).first()
    return db.session.query(User, func.sum(Bet.total_points).label("total_points"), Match) \
        .outerjoin(Bet, Bet.user_id == User.id) \
        .outerjoin(Match, Bet.match_id == Match.id) \
        .filter(Match.tournament == tournament_id) \
        .filter(Match.time_start > last_match_time.time_start - datetime.timedelta(hours=12)) \
        .filter(Bet.points is not None) \
        .group_by(Bet.user_id) \
        .order_by(func.sum(Bet.points).desc(), func.count(Bet.points)) \
        .all()
