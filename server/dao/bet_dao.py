from server import models, db
from server.models import Bet


def add_new_bet(user_id, match_id, home_score, away_score):
    bet = Bet.query.filter(Bet.user_id == user_id, Bet.match_id == match_id).first()

    if bet:
        bet.home_team_score = home_score
        bet.away_team_score = away_score
    else:
        bet = Bet(user_id, match_id, home_score, away_score)
        db.session.add(bet)
        db.session.flush()

    db.session.commit()

    return bet

