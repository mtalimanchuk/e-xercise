import json

from flask import (abort, flash, jsonify, redirect, render_template, request,
                   url_for)

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
        title = request.form['exercise-title']
        activities = []

        # TODO add multiple entry forms
        howto = request.form['exercise-howto']
        raw_content = request.form['exercise-content']
        activity = {'howto': howto, 'raw_content': raw_content}
        activities.append(activity)

        if title and len(activities) > 0:
            exercise_id = generator_util.save_exercise(title, activities)
            return redirect(url_for('exercise', exercise_id=exercise_id))
        else:
            flash("Make sure to fill the title and at least 1 activity")
            return redirect(url_for('exercise_generator'))


@app.route("/exercise/<exercise_id>")
def exercise(exercise_id):
    try:
        exercise_title, exercise_activities = generator_util.load_exercise(exercise_id)
        return render_template("exercise.html.j2",
                               exercise_id=exercise_id,
                               exercise_title=exercise_title,
                               exercise_activities=exercise_activities)
    except FileNotFoundError as e:
        print(f"{type(e)}: {e}")
        return abort(404, f"Exercise {exercise_id} doesn't exist :(")


@app.route("/exercise/<exercise_id>/check", methods=["POST"])
def check(exercise_id):
    # https://javascript.info/bubbling-and-capturing
    payload = json.loads(request.data.decode('utf-8'))
    task_id = payload["task_id"]
    student_answer = payload["task_answer"]
    # TODO remove contraction sensitivity (parse "'m" as "am" and so on)
    result = generator_util.check_exercise_answer(exercise_id, task_id, student_answer)

    return jsonify(id=task_id, result=result)
