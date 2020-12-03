from sqlalchemy import Column, ForeignKey, Integer, Text
from storage.database import base
from sqlalchemy.inspection import inspect


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class User(base, Serializer):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d


class Task(base, Serializer):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    completed = Column(Text, nullable=False)

    def __init__(self, id, user_id, title, description, completed):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.completed = completed

    def serialize(self):
        d = Serializer.serialize(self)
        return d
