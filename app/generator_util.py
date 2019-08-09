import json
import re
import uuid


CONTRACTIONS = {
    "am": "'m",
    "is": "'s",
    "is not": "isn't",
    "are": "'re",
    "are not": "aren't",
    "have": "'ve",
    "have not": "haven't",
    "has": "'s",
    "has not": "hasn't",
    "will": "'ll",
    "will not": "won't"
}


def save_exercise_json(raw_input):
    exercise_id = uuid.uuid4()
    tokens = list(_parse_generator_input(raw_input))
    with open(f"exercisedb/{exercise_id}.json", 'w', encoding='utf-8') as save_f:
        json.dump(tokens, save_f)
    return exercise_id


def load_exercise_json(id):
    with open(f"exercisedb/{id}.json", 'r', encoding='utf-8') as load_f:
        exercise_content = json.load(load_f)
    return exercise_content


def check_exercise_answer(exercise_id, task_id, student_answer):
    exercise = load_exercise_json(exercise_id)
    for sentence in exercise:
        for token in sentence:
            if token.get('task_id') == task_id and student_answer in token.get('correct_answers'):
                return True
    return False


def _parse_generator_input(raw_input):
    _raw_sentences = [line for line in raw_input.split('\n') if line.strip() != '']
    for _raw_sent in _raw_sentences:
        sent = _raw_sent.replace('\n', '')
        tokens = [t for t in re.split(r"(<.*?>)", sent) if t != '']
        tokens = list(_parse_sentence_tokens(tokens))
        yield tokens


def _parse_sentence_tokens(token_list):
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
            try:
                placeholder = re.findall(r"\(.*?\)", _raw_task)[0][1:-1]
            except IndexError:
                placeholder = None
            answer_options = re.sub(r"\(.*?\)", '', _raw_task).split("|")
            token = {"type": "kb_input",
                     "task_id": str(uuid.uuid4()),
                     "placeholder": placeholder,
                     "correct_answers": answer_options}

        else:
            token = {"type": "plaintext",
                     "content": t}
        yield token


if __name__ == '__main__':
    check_exercise_answer("e27b4180-4268-4066-82e7-54424e6a1d4d",
                          "d4daf6f9-5a55-4cf9-bb53-1290b829642c",
                          student_answer='was')
