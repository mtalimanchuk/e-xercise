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


def _add_exercise_to_db(input_entity):
    task_id = input_entity['task_id']
    correct_answers = input_entity['correct_answers']
    with open('test_db.txt', 'a', encoding='utf-8') as placeholder_db:
        placeholder_db.write(f"{task_id}={correct_answers}\n")


def _check_exercise_in_db(task_id, student_answer):
    with open('test_db.txt', 'r', encoding='utf-8') as placeholder_db:
        answers = list(placeholder_db)
        for answer in answers:
            _task_id, _correct_answer = answer.split('=')
            if _task_id == task_id:
                return student_answer in [a.strip()[1:-1] for a in _correct_answer.strip("[]\n").split(",")]


def parse_exercise_markup(raw_text):
    # TODO possibly add auto-(de)capitalization to answers
    """ Markup rules:
    <> - Task wrapper.
        Contents may include:
        | - delimiter for possible answers, e.g. He <will|is going to> play basketball tomorrow
        () - input placeholder, e.g. She <is(be)> ready

    """
    raw_tokens = re.split(r"(<.*?>)", raw_text)
    for token in raw_tokens:
        if token.startswith("<") and token.endswith(">"):
            raw_exercise = token[1:-1]
            try:
                placeholder = re.findall(r"\(.*?\)", raw_exercise)[0][1:-1]
            except IndexError:
                placeholder = None
            answer_options = re.sub(r"\(.*?\)", '', raw_exercise).split("|")
            classified_token = {"type": "kb_input",
                                "task_id": str(uuid.uuid4()),
                                "placeholder": placeholder,
                                "correct_answers": answer_options}
            _add_exercise_to_db(classified_token)

        else:
            classified_token = {"type": "plaintext",
                                "content": token}

        yield classified_token


if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter()

    ents = parse_exercise_markup("My name <is(be)> Miguel and I <am> from Penza. I think it <will> be important in the future. How <was|is> your mother doing?")

    pp.pprint([e for e in ents])
