#!/usr/bin/python3

import argparse
import logging

from flask import Flask, render_template

from db.database import ClassroomDb

"""COMMAND LINE ARGUMENTS"""


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='ip',
                        help='Optional. IP address to bind the server to. Default is 127.0.0.1')
    parser.add_argument('-p', '--port', dest='port',
                        help='Optional. Port to listen for the server. Default is 5000/tcp')
    parser.add_argument('-l', '--logging', dest='log_level',
                        help='Optional. Logging level to use in application. '
                             'Can be one of the following: [INFO, DEBUG, WARN, ERROR]. Default is INFO.')

    options = parser.parse_args()
    if not options.ip:
        options.ip = '127.0.0.1'
    if not options.port:
        options.port = 5000
    if not options.log_level:
        options.log_level = 'INFO'

    return options


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

DB_SCHEMA_FILE = './db/schema.sql'
DB_TEST_DATA_FILE = './db/data.sql'

db = ClassroomDb(db_host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, db_name=DB_NAME)
db.init_schema(DB_SCHEMA_FILE)
db.init_test_data(DB_TEST_DATA_FILE)
"""ROUTES AND HANDLERS"""


# when we reach here, we should already have an initialized data access object

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


"""APPLICATION STARTUP"""
if __name__ == '__main__':
    app.run(host=options.ip, port=options.port)
