#!/usr/bin/python3

"""DATABASE MODELS"""


class BaseModel:
    def __init__(self):
        self.id = None

    def is_new(self):
        return self.id is None


class Student(BaseModel):
    def __init__(self):
        super().__init__()
        self.username = None
        self.unique_url = None
        self.is_active = None


class Task(BaseModel):
    def __init__(self):
        super().__init__()
        self.content = None


class Assigment(BaseModel):
    def __init__(self):
        super().__init__()
        self.task_id = None
        self.student_id = None
        self.is_completed = False
        self.completion_timestamp = None
