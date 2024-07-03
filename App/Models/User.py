from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, JSON, Integer, Enum
import enum
import os
from glob import glob
from flask import current_app as app


class Role(enum.Enum):
    ADMIN = "ADMIN"
    pass


class User(Base, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(Enum(Role))
    name = Column(String(255))
    photo = Column(String(255))
    flag = Column(Integer, default=1)

    def getPhotoProfile(self):
        path = app.root_path + "/static/profiles/" + self.username + ".png"

        if os.path.exists(path):
            return "/Static/profiles/" + self.username + ".png"
        else:
            return ""

    pass


def _hashPassword(plaintext):
    return md5(str(plaintext).encode()).hexdigest()


def _fetchByUsername(username):
    return User.query.filter(User.username == username, User.flag == 1).first()


def _fetchById(id):
    return User.query.filter(User.id == id, User.flag == 1).first()
