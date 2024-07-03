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
    accuracy = Column(String(10), nullable=True)
    total_data = Column(Integer, nullable=True)
    total_benar = Column(Integer, nullable=True)
    file_result = Column(String(255), nullable=True)

    def getPathFile(self):
        return url_for("static", filename="uploads/source/" + self.file, _external=True)
    pass

    def getPathResult(self):
        return url_for(
            "static", filename="uploads/result/" + self.file_result, _external=True)
    pass


pass


def ActiveQuery():
    return Uploader.query


def fetchOne(id):
    return Uploader.query.filter(Uploader.id == id).first()


def assign(form):
    return Uploader(
        nama=form['name'],
        file=form['file'],
        accuracy=form['accuracy'],
        total_data=form['total_data'],
        total_benar=form['total_benar'],
        file_result=form['file_result'],
    )


def modify(model, form):
    for key, val in form.items():
        if hasattr(model, key):
            setattr(model, key, val)
