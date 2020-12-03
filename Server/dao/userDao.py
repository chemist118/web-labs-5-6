from entities.models import User
from werkzeug.security import generate_password_hash
from storage.database import db_session


def add_user(login, password):
    db_session.add(User(None, login, generate_password_hash(password, salt_length=64)))
    db_session.commit()


def get_user_by_id(user_id):
    return User.query.filter(User.id == user_id).first()


def get_user_by_login(login):
    return User.query.filter(User.login == login).first()


def get_users():
    return User.query


