import json
from pathlib import Path
import re

import shortuuid


_db = Path("db")
EXERCISE_DIR = _db / "exercise"
ANSWERKEY_DIR = _db / "answerkey"
EXERCISE_DIR.mkdir(exist_ok=True, parents=True)
ANSWERKEY_DIR.mkdir(exist_ok=True, parents=True)

# https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
# https://pythonhosted.org/Flask-FormEncode/
input_sanitizing_rules = [
    ("&", "&amp;"),
    ("<", "&lt;"),
    (">", "&gt;"),
    ('"', "&quot;"),
    ("'", "&#39;"),
    ("/", "&#x2F"),
]


def _sanitize_input(form_input):
    for rule in input_sanitizing_rules:
        form_input = form_input.replace(*rule)
    return form_input


class Exercise:
    def __init__(self, title, raw_activities):
        self.title = _sanitize_input(title)
        self.id = shortuuid.ShortUUID().random(length=10)
        self.answer_keys = {}
        self.activities = []
        for activity in raw_activities:
            howto = _sanitize_input(activity["howto"])
            raw_content = activity["raw_content"]  # sanitize also?
            tokens = list(self._parse_generator_input(raw_content))
            self.activities.append({"howto": howto, "content": tokens})
        self._exercise_path = _db / "exercise" / f"{self.id}.json"
        self._answerkey_path = _db / "answerkey" / f"{self.id}.json"
        self.json = {"title": self.title, "activities": self.activities}

    def _parse_generator_input(self, raw_input):
        _raw_sentences = [line for line in raw_input.split("\n") if line.strip() != ""]
        for _raw_sent in _raw_sentences:
            sent = _raw_sent.replace("\n", "")
            tokens = [t for t in re.split(r"(<.*?>)", sent) if t != ""]
            tokens = list(self._parse_sentence_tokens(tokens))
            yield tokens

    def _parse_sentence_tokens(self, token_list):
        # TODO possibly add auto-(de)capitalization to answers
        """ Markup rules:
        <> - Task wrapper.
            Contents may include:
            | - delimiter for possible answers, e.g. He <will|is going to> play basketball tomorrow
            () - input placeholder, e.g. She <is(be)> ready

        """
        for t in token_list:
            if t.startswith("<") and t.endswith(">"):
                _raw_task = t[1:-1]
                task_id = str(shortuuid.ShortUUID().random(length=10))
                try:
                    placeholder = re.findall(r"\(.*?\)", _raw_task)[0][1:-1]
                except IndexError:
                    placeholder = None
                answer_options = re.sub(r"\(.*?\)", "", _raw_task).split("|")
                self.answer_keys[task_id] = answer_options
                token = {
                    "type": "kb_input",
                    "task_id": task_id,
                    "placeholder": placeholder,
                }

            else:
                token = {"type": "plaintext", "text": t}
            yield token


def save_exercise(title, raw_activities):
    e = Exercise(title, raw_activities)
    with open(e._exercise_path, "w", encoding="utf-8") as content_f:
        json.dump(e.json, content_f)
    with open(e._answerkey_path, "w", encoding="utf-8") as answers_f:
        json.dump(e.answer_keys, answers_f)
    return e.id


def load_exercise(exercise_id):
    with open(EXERCISE_DIR / f"{exercise_id}.json", "r", encoding="utf-8") as load_f:
        e = json.load(load_f)
    return e["title"], e["activities"]


def check_exercise_answer(exercise_id, task_id, student_answer):
    with open(ANSWERKEY_DIR / f"{exercise_id}.json", "r", encoding="utf-8") as load_f:
        answers = json.load(load_f)
    return student_answer in answers[task_id]
