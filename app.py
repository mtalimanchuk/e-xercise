#!/usr/bin/python3

import json
import logging
import os
import sys

from flask import Flask, render_template, abort, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

sys.path.append(os.getcwd())

"""APP CONFIGURATION """
ip = '127.0.0.1'
port = 5000

app = Flask(__name__)
logging.basicConfig(format='[%(asctime)s %(levelname)s]: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level='INFO')
basedir = os.path.abspath(os.path.dirname(__file__))

"""DATABASE CONNECTION PROPERTIES """

DB_HOST = 'localhost'
DB_USERNAME = 'classroom'
DB_PASSWORD = 'classroom'
DB_NAME = 'classroom_db'

DB_URL = os.environ.get('DATABASE_URL') or \
         'mysql://' + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST + ':3306/' + DB_NAME


class Config(object):
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    text = db.Column(db.Text(42940000), nullable=False)
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

# when we reach here, we should already have an initialized database layer
"""ROUTES AND HANDLERS"""
API_PREFIX = '/api/v1'


def bad_request(error_message):
    abort(400, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


def not_found(error_message):
    abort(404, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


def ok(message):
    return jsonify({'message': message}), 200


#### PUBLIC RESOURCES:
@app.route("/")
@app.route("/index")
def index():
    return '<a href="/exercise_TestLink">Test</a>'


@app.route("/exercise_<exercise_link>")
def exercise(exercise_link):
    return render_template("exercise.html", exercise_link=exercise_link)


@app.route("/check", methods=["POST"])
def check():

    ANSWERS = {'task1': 'am', 'task2': 'were'}
    check_answer_in_db = lambda _id, _answer: ANSWERS[_id] == _answer

    # https://javascript.info/bubbling-and-capturing
    payload = json.loads(request.data.decode('utf-8'))
    task_id = payload["task_id"]
    task_answer = payload["task_answer"]
    print(payload)
    # TODO remove contraction sensitivity (parse "'m" as "am" and so on)

    submit_result = check_answer_in_db(task_id, task_answer)

    return jsonify(id=task_id, result=submit_result)

# @app.route('/exercise', methods=['GET'])
# def exercise():
#     sentence = Sentence(id=1, lang='aaa', text='aaa')
#     return ok(sentence)


if __name__ == '__main__':
    app.run(host=ip, port=port)
