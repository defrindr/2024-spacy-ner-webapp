from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import url_for, current_app as app


class Crawler(Base, db.Model):
    __tablename__ = 'crawler'

    id = Column(Integer, primary_key=True)
    result = Column(String(255))
    keyword = Column(String(255))
    limit = Column(Integer())
    # jumlah_data = Column(Integer())

    def getPathResult(self):
        return url_for(
            "static", filename=self.result, _external=True)
    pass


pass


def ActiveQuery():
    return Crawler.query


def fetchOne(id):
    return Crawler.query.filter(Crawler.id == id).first()


def assign(form):
    return Crawler(
        keyword=form['keyword'],
        limit=form['limit'],
        result=form['result'],
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
