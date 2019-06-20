#!/usr/bin/python3

import argparse
import logging

from flask import Flask, render_template

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


"""CONFIGURATION """
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

"""DATABASE LAYER INITIALIZATION"""
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

"""ROUTES AND HANDLERS"""


# when we reach here, we should already have an initialized database layer

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host=options.ip, port=options.port)
