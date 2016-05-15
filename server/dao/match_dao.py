import datetime

from sqlalchemy import and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.operators import as_

from server import models, db
from server.models import Match, Bet, User


def add_match(tournament, home_team, away_team, time_start):
    match = models.Match(tournament=tournament, home_team=home_team, away_team=away_team, time_start=time_start)
    db.session.add(match)
    db.session.commit()


def get_match_by_id(match_id):
    return Match.query.filter(Match.id == match_id).first()


def get_nearest_matches_and_bets_by_user(user_id):
    now = datetime.datetime.utcnow()
    return db.session.query(Match, Bet)\
        .outerjoin(Bet, and_(Bet.match_id == Match.id, Bet.user_id == user_id))\
        .filter(Match.time_start > now)\
        .all()


def get_past_matches_and_bets_by_user(user_id):
    now = datetime.datetime.utcnow()
    return db.session.query(Match, Bet)\
        .outerjoin(Bet, and_(Bet.match_id == Match.id, Bet.user_id == user_id))\
        .filter(Match.time_start < now)\
        .all()


def get_past_matches_and_bets_by_tournament(tournament_id):
    now = datetime.datetime.utcnow()

    users = User.query.order_by(User.id).all()
    qbets = Bet.query.all()

    bets = {}
    for bet in qbets:
        bets.update({bet.id: bet})

    q = db.session.query(Match)

    for user in users:
        bet_alias = aliased(Bet)
        q = q.add_columns(bet_alias.id.label(str(user.id)))
        q = q.outerjoin(bet_alias, and_(bet_alias.match_id == Match.id, user.id == bet_alias.user_id))

    q = q.filter(Match.time_start < now).filter(Match.tournament == tournament_id)
    q = q.order_by(Match.time_start)
    q = q.all()

    match_user_bet = []

    for line in q:
        l = [line[0]]
        for i in range(1, len(line)):
            if line[i] is not None:
                l.append(bets[line[i]])
            else:
                l.append(None)

        match_user_bet.append(l)

    """
        users - list of Users :  [User1, User2, User3]

        match_user_bet - table (list of lists) of Bets :
            [
                [Match1, Bet of User1, Bet of User2, Bet of User3]
                [Match2, Bet of User1, Bet of User2, Bet of User3]
                [Match3, Bet of User1, Bet of User2, Bet of User3]
            ]
    """

    return users, match_user_bet

