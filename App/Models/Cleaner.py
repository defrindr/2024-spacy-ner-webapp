from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import url_for, current_app as app


class Cleaner(Base, db.Model):
    __tablename__ = 'cleaner'

    id = Column(Integer, primary_key=True)
    file = Column(String(255))
    result = Column(String(255))

    def getPathFile(self):
        return url_for("static", filename=self.file, _external=True)
    pass

    def getPathResult(self):
        return url_for(
            "static", filename=self.result, _external=True)
    pass


pass


def ActiveQuery():
    return Cleaner.query


def fetchOne(id):
    return Cleaner.query.filter(Cleaner.id == id).first()


def assign(form):
    return Cleaner(
        file=form['file'],
        result=form['result'],
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
