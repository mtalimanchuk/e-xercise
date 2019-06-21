#!/usr/bin/python3

# import hack: https://stackoverflow.com/a/45874916/8325160
import sys

sys.path.append('..')

from db.database import ClassroomDb
from db.dao.model import Task
import logging


class TaskDao(ClassroomDb):
    @staticmethod
    def row_mapper(row):
        if not row or row == '':
            raise Exception("Task database row passed to be mapped on the python object is null ")
        task = Task()
        task.id = row[0]
        task.content = row[1]
        return task

    def save(self, content):
        super().validate_varchar(content, "task content", 1024)
        query = f"INSERT INTO task (content) " \
            f"VALUES ('{content}')"
        return super().execute_statement(query)

    def get(self, id):
        super().validate_id(id, 'task')
        logging.debug('Get a task: %s' % id)
        query = "SELECT * FROM task WHERE id = %s" % id
        raw_data = super().query_for_object(query)
        if raw_data:
            return self.row_mapper(raw_data)

    def get_all(self):
        logging.debug('Get all tasks')
        query = "SELECT * FROM task"
        raw_data = super().query_for_list(query)
        if raw_data:
            return [self.row_mapper(row) for row in raw_data]

    def delete(self, id):
        super().validate_id(id, 'task')
        logging.debug('Delete a task %s' % id)

        logging.debug("Deleting task's [%s] assignments" % id)
        query = "DELETE FROM assignment WHERE task_id = %s" % id
        super().execute_statement(query)

        logging.debug('Deleting a task %s' % id)
        query = "DELETE FROM task WHERE id = %s" % id
        return super().execute_statement(query)
