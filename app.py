#!/usr/bin/python3

import argparse

from flask import Flask, render_template


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', dest='ip',
                        help='Optional. IP address to bind the server to. Default is 127.0.0.1')
    parser.add_argument('-p', '--port', dest='port',
                        help='Optional. Port to listen for the server. Default is 5000/tcp')

    options = parser.parse_args()
    if not options.ip:
        options.ip = '127.0.0.1'
    if not options.port:
        options.port = 5000

    return options


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    options = get_arguments()
    app.run(host=options.ip, port=options.port)
