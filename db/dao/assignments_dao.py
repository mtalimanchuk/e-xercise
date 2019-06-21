#!/usr/bin/python3

# import hack: https://stackoverflow.com/a/45874916/8325160
import sys

sys.path.append('..')

from db.database import ClassroomDb
from db.dao.model import Assignment
import logging


class AssignmentDao(ClassroomDb):
    @staticmethod
    def row_mapper(row):
        if not row or row == '':
            raise Exception("Assignment database row passed to be mapped on the python object is null ")
        assignment = Assignment()
        assignment.id = row[0]
        assignment.student_id = row[1]
        assignment.task_id = row[2]
        assignment.is_completed = row[3]
        assignment.completion_timestamp = row[4]
        return assignment

    def assign(self, student_id, task_id):
        super().validate_id(student_id, "student")
        super().validate_id(task_id, "task")

        query = f"INSERT INTO assignment (student_id, task_id) " \
            f"VALUES ({student_id}, {task_id})"
        return super().execute_statement(query)

    def complete_task(self, student_id, task_id):
        super().validate_id(student_id, "student")
        super().validate_id(task_id, "task")

        query = f'UPDATE assignment ' \
            f'SET is_completed = 1, ' \
            f'completion_timestamp = NOW() ' \
            f'WHERE student_id = {student_id} AND task_id = {task_id}'
        return super().execute_statement(query)

    def get(self, id):
        super().validate_id(id, 'assignment')
        logging.debug('Get an assignment: %s' % id)
        query = "SELECT * FROM assignment WHERE id = %s" % id
        raw_data = super().query_for_object(query)
        if raw_data:
            return self.row_mapper(raw_data)

    def get_all(self):
        logging.debug('Get all assignments')
        query = "SELECT * FROM assignment"
        raw_data = super().query_for_list(query)
        if raw_data:
            return [self.row_mapper(row) for row in raw_data]

    def delete(self, id):
        super().validate_id(id, 'assignment')

        logging.debug("Deleting an assignment with id %s" % id)
        query = "DELETE FROM assignment WHERE id = %s" % id
        return super().execute_statement(query)
