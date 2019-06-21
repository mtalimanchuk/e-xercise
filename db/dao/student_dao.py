#!/usr/bin/python3

import logging
# import hack: https://stackoverflow.com/a/45874916/8325160
import sys

sys.path.append('..')

from db.database import ClassroomDb
from db.dao.model import Student
import uuid


class StudentDao(ClassroomDb):
    """Transform a raw database data to the python object"""

    @staticmethod
    def row_mapper(row):
        if not row or row == '':
            raise Exception("Student database row passed to be mapped on python model is null")
        student = Student()
        student.id = row[0]
        student.username = row[1]
        student.is_active = row[2]
        student.unique_url = row[3]
        return student

    @staticmethod
    def generate_unique_url():
        return uuid.uuid4().hex + uuid.uuid4().hex

    def save(self, username):
        super().validate_varchar(username, "student username")
        query = f"INSERT INTO student (username, is_active, unique_url) " \
            f"VALUES ('{username}',{1}, '{self.generate_unique_url()}')"
        return super().execute_statement(query)

    def get(self, id):
        super().validate_id(id, 'student')
        logging.debug('Get a student, id: [%s]' % id)
        query = "SELECT * FROM student WHERE id = %s" % id
        raw_data = super().query_for_object(query)
        if raw_data:
            return self.row_mapper(raw_data)

    def get_all(self):
        logging.debug('Get all students')
        query = "SELECT * FROM student"
        raw_data = super().query_for_list(query)
        if raw_data:
            return [self.row_mapper(row) for row in raw_data]

    def delete(self, id):
        super().validate_id(id, 'student')
        logging.debug('Delete a user %s' % id)

        logging.debug("Deleting user's [%s] assignments" % id)
        query = "DELETE FROM assignments WHERE student_id = %s" % id
        super().execute_statement(query)

        logging.debug('Deleting a user %s' % id)
        query = "DELETE FROM student WHERE id = %s" % id
        return super().execute_statement(query)

