#!/bin/bash

path=$(pwd)/app.py
mode=development
#use it with a fresh database

export FLASK_APP=$path
export FLASK_ENV=$mode

rm -rf ./migrations

flask db init
flask db migrate -m "create schema"
flask db upgrade
