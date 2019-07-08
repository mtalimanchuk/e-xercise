import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_HOST = 'localhost'
    DB_USERNAME = 'classroom'
    DB_PASSWORD = 'classroom'
    DB_NAME = 'classroom_db'

    DB_URL = os.environ.get('DATABASE_URL') or \
             'mysql://' + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST + ':3306/' + DB_NAME
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False