import json
from flask import render_template, render_template_string, abort, jsonify, request, redirect, url_for
from app import app


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
        from uuid import uuid4
        exercise_id = uuid4()
        exercise_data = request.form['gen_input']
        with open(f"exercisedb/{exercise_id}.txt", 'w', encoding='utf-8') as exc_f:
            exc_f.write(exercise_data)
        return redirect(url_for('exercise', exercise_link=exercise_id))


@app.route("/text_lemmatizer")
def text_lemmatizer():
    return render_template("lemmatizer.html.j2")


@app.route("/exercise/<exercise_link>")
def exercise(exercise_link):
    from . import generator_util
    with open(f"exercisedb/{exercise_link}.txt", 'r', encoding='utf-8') as exercise_input:
        content = exercise_input.read()
    content_entities = generator_util.parse_exercise_markup(content)

    return render_template("exercise.html.j2", exercise_link=exercise_link, exercise_content=content_entities)


@app.route("/check", methods=["POST"])
def check():
    from . import generator_util

    # https://javascript.info/bubbling-and-capturing
    payload = json.loads(request.data.decode('utf-8'))
    task_id = payload["task_id"]
    student_answer = payload["task_answer"]
    app.logger.info(payload)
    # TODO remove contraction sensitivity (parse "'m" as "am" and so on)

    submit_result = generator_util._check_exercise_in_db(task_id, student_answer)

    return jsonify(id=task_id, result=submit_result)
