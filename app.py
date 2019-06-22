#!/usr/bin/python3

import argparse
import logging

from flask import Flask, render_template, request, abort, jsonify

from db.dao.assignments_dao import AssignmentDao
from db.dao.student_dao import StudentDao
from db.dao.task_dao import TaskDao
from db.database import ClassroomDb

"""COMMAND LINE ARGUMENTS"""


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='ip', default='127.0.0.1',
                        help='Optional. IP address to bind the server to. Default is 127.0.0.1')
    parser.add_argument('-p', '--port', dest='port', default=5000,
                        help='Optional. Port to listen for the server. Default is 5000/tcp')
    parser.add_argument('-l', '--logging', dest='log_level', default=logging.INFO,
                        choices=['INFO', 'DEBUG', 'WARN', 'ERROR'],
                        help='Optional. Logging level to use in application. '
                             'Can be one of the following: [INFO, DEBUG, WARN, ERROR]. Default is INFO.')

    return parser.parse_args()


"""APP CONFIGURATION """
options = get_arguments()
app = Flask(__name__)
logging.basicConfig(format='[%(asctime)s %(levelname)s]: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=options.log_level)

"""DATABASE CONNECTION PROPERTIES """
# FIXME: replace with a config file
DB_HOST = 'localhost'
DB_USERNAME = 'classroom'
DB_PASSWORD = 'classroom'
DB_NAME = 'classroom_db'

# FIXME: this is for the dev environment and should be removed before going live
db = ClassroomDb(db_host=DB_HOST,
                 username=DB_USERNAME,
                 password=DB_PASSWORD,
                 db_name=DB_NAME,
                 log_level=options.log_level)
DB_SCHEMA_FILE = './db/schema.sql'
DB_TEST_DATA_FILE = './db/data.sql'

db.init_schema(DB_SCHEMA_FILE)
db.init_test_data(DB_TEST_DATA_FILE)

"""DATA ACCESS OBJECTS"""
# tasks crud operations
task_dao = TaskDao(db_host=DB_HOST,
                   username=DB_USERNAME,
                   password=DB_PASSWORD,
                   db_name=DB_NAME,
                   log_level=options.log_level)
# students crud operations
student_dao = StudentDao(db_host=DB_HOST,
                         username=DB_USERNAME,
                         password=DB_PASSWORD,
                         db_name=DB_NAME,
                         log_level=options.log_level)
# assignments tasks to students crud operations
assignment_dao = AssignmentDao(db_host=DB_HOST,
                               username=DB_USERNAME,
                               password=DB_PASSWORD,
                               db_name=DB_NAME,
                               log_level=options.log_level)

# when we reach here, we should already have an initialized database layer
"""ROUTES AND HANDLERS"""
API_PREFIX = '/api/v1'
STUDENTS_URL = API_PREFIX + '/students'


def bad_request(error_message):  # 400 - bad request ;)
    abort(400, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


def not_found(error_message):  # 404 - not found ;)
    abort(404, {"message": error_message})  # FIXME: missing proper Content-Type header, it should be application/json


#### STUDENTS:
# CREATE NEW STUDENTS
@app.route(STUDENTS_URL, methods=['POST'])
def create_student():
    post_data = request.json
    if not post_data:
        bad_request("Either the request body is missing or json is incorrect")
    if 'students' not in post_data:
        bad_request("Missing 'students' list in the post data")
    if len(post_data['students']) == 0:
        bad_request('List of students cannot be empty. You have to send at least one username')

    students = post_data['students']
    logging.info('Create new student(s): %s' % students)

    created_students = [s for s in students if student_dao.save(s)]
    status_code = 201 if len(created_students) > 0 else 204  # 201 - created, 204 - no content ;)
    return jsonify(created_students=created_students), status_code


# GET STUDENTS
@app.route(STUDENTS_URL, methods=['GET'])
def get_student():
    username = request.args.get('username')
    # get one
    if username:
        if ';' in username or '#' in username or '|' in username or '--' in username:
            bad_request('I can break rules, too. Goodbye')
        logging.info("Get a student: %s" % username)
        student = student_dao.get_by_username(username)
        if not student:
            not_found(f'Student "{username}" not found')
        return jsonify(students=student.to_resource()), 200
    # get all
    if not username:
        all_students = [s.to_resource() for s in student_dao.get_all()]
        return jsonify(students=all_students), 200


#### PUBLIC RESOURCES:
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host=options.ip, port=options.port)
