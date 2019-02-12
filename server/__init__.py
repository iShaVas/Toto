from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from config import basedir

app = Flask(__name__, static_folder=os.path.join(basedir, 'static'), template_folder=os.path.join(basedir, 'templates'))

app.config.from_object('config')
app.config['DEBUG'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.secret_key = '\x06\x94\xcf\xaf\xaeB&\xd1s\xa8ZGU\xd2J\xf3\xd6\x12(\xbd\xf5\xc3\x858'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from server import views
