from server import models, db
from server.models import User


def register_user(first_name, last_name, email, nickname, password):
    user = models.User(nickname=nickname, email=email, first_name=first_name, last_name=last_name, password=password)
    db.session.add(user)
    db.session.commit()


def get_user_by_nickname(nickname):
    return User.query.filter(User.nickname == nickname).first()
