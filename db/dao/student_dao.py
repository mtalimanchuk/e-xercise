#!/usr/bin/python3

import logging
# import hack: https://stackoverflow.com/a/45874916/8325160
import sys

sys.path.append('..')

from database import ClassroomDb
from model import Student


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

    def save(self, student):
        pass

    def get(self, id):
        if not id:
            raise Exception("Student id cannot be null")
        try:
            int(id)
        except:
            raise Exception("Student id [%s] cannot be casted to int." % id)
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
        pass


DB_HOST = 'localhost'
DB_USERNAME = 'classroom'
DB_PASSWORD = 'classroom'
DB_NAME = 'classroom_db'

student_dao = StudentDao(db_host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, db_name=DB_NAME)

students = student_dao.get_all()
