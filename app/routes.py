import json
from flask import render_template, abort, jsonify, request
from app import app


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
    return '<a href="/exercise/TestLink">Test</a>'


@app.route("/exercise/<exercise_link>")
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
    app.logger.info(payload)
    # TODO remove contraction sensitivity (parse "'m" as "am" and so on)

    submit_result = check_answer_in_db(task_id, task_answer)

    return jsonify(id=task_id, result=submit_result)
