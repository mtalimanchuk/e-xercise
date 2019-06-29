#!/usr/bin/python3

import argparse
import logging
from flask import jsonify

from flask import Flask, render_template, abort
import sys,os
sys.path.append(os.getcwd())
"""COMMAND LINE ARGUMENTS"""


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='ip', default='127.0.0.1',
                        help='Optional. IP address to bind the server to. Default is 127.0.0.1')
    parser.add_argument('-p', '--port', dest='port', default=5000,
                        help='Optional. Port to listen for the server. Default is 5000/tcp')
    parser.add_argument('-l', '--logging', dest='log_level', default=logging.INFO,
                        choices=['INFO', 'DEBUG', 'WARN', 'ERROR'],
                        help='Optional. Logging level to use in application. '
                             'Can be one of the following: [INFO, DEBUG, WARN, ERROR]. Default is INFO.')

    return parser.parse_args()


"""APP CONFIGURATION """
options = get_arguments()
app = Flask(__name__)
logging.basicConfig(format='[%(asctime)s %(levelname)s]: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=options.log_level)
basedir = os.path.abspath(os.path.dirname(__file__))

"""DATABASE CONNECTION PROPERTIES """
# FIXME: replace with a env variable

DB_HOST = 'localhost'
DB_USERNAME = 'classroom'
DB_PASSWORD = 'classroom'
DB_NAME = 'classroom_db'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql://' + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST + ':3306/' + DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

config = Config()
app.config.from_object(config)
db = SQLAlchemy(app)

"""ORM"""
LIST_ENTITY_NAME = 'List'
LIST_REFERENCE = 'list.id'
LIST_BACK_REFERENCE = 'list'

SENTENCE_ENTITY_NAME = 'Sentence'
SENTENCE_REFERENCE = 'sentence.id'
SENTENCE_BACK_REFERENCE = 'sentence'

EXERCISE_ENTITY_NAME = 'Exercise'
EXERCISE_REFERENCE = 'exercise.id'
EXERCISE_BACK_REFERENCE = 'exercise'

TASKS_ENTITY_NAME = 'Task'


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    lang = db.Column(db.String(3), index=True, nullable=False)
    text = db.Column(db.String(100), index=True, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(LIST_REFERENCE), nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey(EXERCISE_REFERENCE), nullable=True)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(300), nullable=False)

    sentences = db.relationship(SENTENCE_ENTITY_NAME, backref=LIST_BACK_REFERENCE, lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    student_url = db.Column(db.String(30), unique=True, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(LIST_REFERENCE), nullable=True)
    expiration_datetime = db.Column(db.TIMESTAMP, nullable=False)

    sentences = db.relationship(EXERCISE_ENTITY_NAME, backref=SENTENCE_BACK_REFERENCE, lazy=True)
    tasks = db.relationship(TASKS_ENTITY_NAME, backref=EXERCISE_BACK_REFERENCE, lazy=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey(EXERCISE_REFERENCE), nullable=False, unique=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey(SENTENCE_REFERENCE), nullable=False)
    correct_answer = db.Column(db.String(50), nullable=False)
    task_input = db.Column(db.String(50), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    failed_attempts = db.Column(db.Integer, nullable=False, default=0)


class SentenceToList(db.Model):
    sentence_id = db.Column(db.Integer, db.ForeignKey(SENTENCE_REFERENCE), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey(LIST_REFERENCE), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint(sentence_id, list_id),
        {}
    )

migrate = Migrate(app, db)

db.create_all()


# when we reach here, we should already have an initialized database layer
"""ROUTES AND HANDLERS"""
API_PREFIX = '/api/v1'
STUDENTS_URL = API_PREFIX + '/students'


def bad_request(error_message):
    abort(400, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


def not_found(error_message):
    abort(404, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json

def ok(message):
    return jsonify({'message': message}), 200

#### PUBLIC RESOURCES:
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/exercise', methods=['GET'])
def exercise():
    sentence = Sentence(id=1, lang='aaa', text='aaa')
    return ok(sentence)


if __name__ == '__main__':
    app.run(host=options.ip, port=options.port)
