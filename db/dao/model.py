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

    def to_resource(self):
        return \
            {"username": self.username,
             "is_active": True if self.is_active == 1 else False,
             "unique_url": self.unique_url}


class Task(BaseModel):
    def __init__(self):
        super().__init__()
        self.content = None

    def to_resource(self):
        return \
            {"content": self.content}


class Assignment(BaseModel):
    def __init__(self):
        super().__init__()
        self.task_id = None
        self.student_id = None
        self.is_completed = False
        self.completion_timestamp = None

    def to_resource(self):
        return \
            {
                "task_id": self.task_id,
                "student_id": self.student_id,
                "is_completed": True if self.is_completed == 1 else False,
                "completion_timestamp": self.completion_timestamp
                # FIXME: format timestamp to string here or flask can handle it by itself?
            }
