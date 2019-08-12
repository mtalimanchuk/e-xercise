import json

from flask import render_template, render_template_string, abort, jsonify, request, redirect, url_for

from app import app
from . import generator_util

def bad_request(error_message):
    abort(400, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


def not_found(error_message):
    abort(404, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


def ok(message):
    return jsonify({'message': message}), 200


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html.j2")


@app.route("/exercise_generator")
def exercise_generator():
    return render_template("generator.html.j2")


@app.route("/exercise_generator/generate", methods=["POST"])
def generate_exercise():
    if request.method == 'POST':
        exercise_title = request.form['exercise-title']
        exercise_howto = request.form['exercise-howto']
        exercise_content = request.form['exercise-content']
        print(exercise_title, exercise_howto)
        exercise_id = generator_util.save_exercise_json(exercise_content)
        return redirect(url_for('exercise', exercise_id=exercise_id))


@app.route("/text_lemmatizer")
def text_lemmatizer():
    return render_template("lemmatizer.html.j2")


@app.route("/exercise/<exercise_id>")
def exercise(exercise_id):
    exercise_content = generator_util.load_exercise_json(exercise_id)
    return render_template("exercise.html.j2", exercise_id=exercise_id, exercise_content=exercise_content)


@app.route("/exercise/<exercise_id>/check", methods=["POST"])
def check(exercise_id):
    # https://javascript.info/bubbling-and-capturing
    payload = json.loads(request.data.decode('utf-8'))
    task_id = payload["task_id"]
    student_answer = payload["task_answer"]
    # TODO remove contraction sensitivity (parse "'m" as "am" and so on)
    result = generator_util.check_exercise_answer(exercise_id, task_id, student_answer)

    return jsonify(id=task_id, result=result)
