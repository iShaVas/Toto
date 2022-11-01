import datetime
import math
from jinja2 import Template
from sqlalchemy import and_
from server import models, db
from server.models import Match, Bet, User

template = Template("""
# Generation started on {{ now() }}
... this is the rest of my template...
# Completed generation.
""")

template.globals['now'] = datetime.datetime.utcnow


def add_match(tournament, home_team, away_team, time_start):
    match = models.Match(tournament=tournament, home_team=home_team, away_team=away_team, time_start=time_start)
    db.session.add(match)
    db.session.commit()


def get_match_by_id(match_id):
    return Match.query.filter(Match.id == match_id).first()


def get_nearest_matches_and_bets_by_user(user_id):
    now = datetime.datetime.utcnow()
    return db.session.query(Match, Bet) \
        .outerjoin(Bet, and_(Bet.match_id == Match.id, Bet.user_id == user_id)) \
        .filter(Match.time_start > now) \
        .order_by(Match.time_start) \
        .all()


def get_past_matches_and_bets_by_user(user_id):
    now = datetime.datetime.utcnow()
    return db.session.query(Match, Bet) \
        .outerjoin(Bet, and_(Bet.match_id == Match.id, Bet.user_id == user_id)) \
        .filter(Match.time_start < now) \
        .order_by(Match.time_start.desc()) \
        .all()


def add_result(match_id, home_team_score, away_team_score):
    match = Match.query.filter(Match.id == match_id).first()
    match.home_team_score = home_team_score
    match.away_team_score = away_team_score

    bets = Bet.query.filter(Bet.match_id == match_id).all()
    for bet in bets:
        bet.points, bet.total_points = calculate_user_points(home_team_score, away_team_score,
                                                             bet.home_team_score, bet.away_team_score, 1) # Edit here

    db.session.commit()


def get_past_matches_and_bets_by_tournament(tournament_id):
    users_list = User.query.order_by(User.id).all()

    data = db.session.query(Match, Bet, User) \
        .outerjoin(Bet, Bet.match_id == Match.id) \
        .outerjoin(User, Bet.user_id == User.id) \
        .filter(Match.tournament == tournament_id) \
        .order_by(Match.time_start.desc()) \
        .all()

    dic = {}

    for match, bet, user in data:
        match_data = {}
        if match.id in dic:
            match_data = dic[match.id]['users']
        else:
            dic[match.id] = {'match': match}
        if user:
            match_data.update({user.id: {'user': user, 'bet': bet}})
            dic[match.id]['users'] = match_data

    array = []
    for k, v in dic.items():
        array.append(v)

    for match in array:
        if 'users' in match:
            users = match['users']
        else:
            users = {}

        for user in users_list:
            if user.id not in users:
                users.update({user.id: {'user': user, 'bet': None}})

        match['users'] = users

    array = sorted(array, key=lambda m: m['match'].time_start, reverse=True)

    return users_list, array


def calculate_user_points(match_home_score, match_away_score, bet_home_score, bet_away_score, multiplier):
    points = 0
    if match_home_score - match_away_score > 0 and bet_home_score - bet_away_score > 0 \
            or match_home_score - match_away_score == 0 and bet_home_score - bet_away_score == 0\
            or match_home_score - match_away_score < 0 and bet_home_score - bet_away_score < 0:

        points += 3

        if match_home_score - match_away_score == bet_home_score - bet_away_score:
            points += 4

            if math.fabs(match_home_score - match_away_score) >= 3:
                points += 1

        if abs((match_home_score - match_away_score) - (bet_home_score - bet_away_score)) == 1:
            points += 2

        if match_home_score == bet_home_score and match_away_score == bet_away_score:
            points += 3

    total_points = points * multiplier

    return points, total_points


def get_unique_tournaments_by_user(user_id):

    tournaments = db.session.query(Match, Bet, User) \
        .outerjoin(Bet, Bet.match_id == Match.id) \
        .outerjoin(User, Bet.user_id == User.id) \
        .filter(User.id == user_id) \
        .group_by(Match.tournament) \
        .all()

    return [tournament.Match.tournament for tournament in tournaments]


def get_matches_by_tournament(tournament):
    return Match.query.filter(Match.tournament == tournament).count()


def get_tournament_matches(tournament):
    matches_list = []
    matches = db.session.query(Match.id).filter(Match.tournament == tournament).all()
    for match in matches:
        matches_list.append(match.id)

    return matches_list