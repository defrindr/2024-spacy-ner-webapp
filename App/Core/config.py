import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # My Config
    BASE_PATH =os.getcwd()
    APP_NAME = os.environ.get('APP_NAME')
    APP_PORT = os.environ.get('APP_PORT')
    APP_NAME_SIMPLE = os.environ.get('APP_NAME_SIMPLE')
    AUTHOR_NAME = os.environ.get('AUTHOR_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQlAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Session Libraru
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    MINIMUM_CONFIDENCE_ATTENDANCE = 60
    MINIMUM_CONFIDENCE_TRAINING = 60
