from server import models, db
from server.models import Match


def add_match(tournament, home_team, away_team, time_start):
    match = models.Match(tournament=tournament, home_team=home_team, away_team=away_team, time_start=time_start)
    db.session.add(match)
    db.session.commit()
