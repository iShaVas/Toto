import datetime
from server import db
from server.models import User


def register_user(first_name, last_name, email, nickname, password):
    register_time = datetime.datetime.now()
    user = User(nickname=nickname, email=email, first_name=first_name, last_name=last_name, password=password,
                register_time=register_time)
    db.session.add(user)
    db.session.commit()


def get_user_by_nickname(nickname):
    return User.query.filter(User.nickname == nickname).first()


def get_all_nicknames():
    user_list = []
    users = db.session.query(User.nickname).all()

    for user in users:
        user_list.append(user.nickname)
    return user_list
