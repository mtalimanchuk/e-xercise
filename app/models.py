from app import db

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

