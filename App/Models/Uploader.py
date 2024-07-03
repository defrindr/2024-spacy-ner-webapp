from hashlib import md5

from .Base import Base
from App.Core.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Text
import enum
import os
from glob import glob
from flask import url_for, current_app as app


class Uploader(Base, db.Model):
    __tablename__ = 'uploaders'

    id = Column(Integer, primary_key=True)
    nama = Column(String(255))
    file = Column(String(255))
    spacy = Column(Text(), nullable=True)
    result = Column(Text(), nullable=True)

    def getPathFile(self):
        return url_for("static", filename=self.file, _external=True)
    pass

    def getPathResult(self):
        return url_for(
            "static", filename=self.spacy, _external=True)
    pass


pass


def ActiveQuery():
    return Uploader.query


def fetchOne(id):
    return Uploader.query.filter(Uploader.id == id).first()


def assign(form):
    return Uploader(
        nama=form['nama'],
        file=form['file'],
        spacy=form['spacy'],
        result=form['result'],
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
