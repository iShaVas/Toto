from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField
from wtforms.validators import equal_to, length, DataRequired
from server.dao.tournament_dao import get_all_tournaments


class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()], _name='first_name')
    last_name = StringField('Last Name', validators=[DataRequired()], _name='last_name')
    nickname = StringField('Last Name', validators=[DataRequired()], _name='nickname')
    password = PasswordField('Password', validators=[DataRequired()], _name='password')
    confirmpass = PasswordField('Confirm', validators=[equal_to('password'), length(max=255)], _name='confirmpass')
    email = StringField('Email', validators=[DataRequired()], _name='email')


class LoginForm(Form):
    nickname = StringField('Nickname', validators=[DataRequired()], _name='nickname')
    password = PasswordField('Password', validators=[DataRequired()], _name='password')


class AddMatchForm(Form):
    tournament = SelectField('Tournament', validators=[DataRequired()], coerce=str)
    home_team = StringField('Home Team', validators=[DataRequired()])
    away_team = StringField('Away Team', validators=[DataRequired()])
    time_start = StringField('Time Start', validators=[DataRequired()])
    date_start = StringField('Time Start', validators=[DataRequired()])
    timezone = SelectField('Time Start', validators=[DataRequired()], choices=[(0, 'UTC+0'), (1, 'UTC+1'), (2, 'UTC+2'),
                                                                               (3, 'UTC+3'), (4, 'UTC+4'), (5, 'UTC+5'),
                                                                               (6, 'UTC+6'), (7, 'UTC+7'),
                                                                               (8, 'UTC+8')], default=3, coerce=int)
    add_match_area = TextAreaField('Add Match Area')

    @classmethod
    def new(cls):
        form = cls()
        tournaments = get_all_tournaments()
        form.tournament.choices = tournaments
        form.tournament.default = tournaments[-1][0]
        return form


class AddTournamentForm(Form):
    name = StringField('Tournament Name', validators=[DataRequired()], _name='name')
    name_full = StringField('Tournament Name Full', validators=[DataRequired()], _name='name')
    date_start = DateField('Date Start', validators=[DataRequired()])
    date_end = DateField('Date End', validators=[DataRequired()])