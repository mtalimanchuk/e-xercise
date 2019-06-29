#!/bin/bash
path=$(pwd)/app.py
mode=development


export FLASK_APP=$path
export FLASK_ENV=$mode
flask run
