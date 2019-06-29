#!/usr/bin/python3
import csv
import logging
from argparse import ArgumentParser

import pymysql

from app import DB_HOST
from app import DB_NAME
from app import DB_PASSWORD
from app import DB_USERNAME

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USERNAME,
                             password=DB_PASSWORD,
                             database=DB_NAME)
connection.autocommit(False)


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-s', '--sentences', dest='sentences',
                        help='CSV file with sentences to import into local db')
    options = parser.parse_args()
    if not options.sentences:
        parser.error('No sentences CSV provided')
    return options


def import_sentences(file_name):
    def read_csv(file_name):
        file = csv.DictReader(open(file_name), delimiter='\t')
        for row in file:
            lang = row['lang']
            text = row['text'].replace('\'', '\\\'')
            logging.info("%s / %s", lang, text)
            connection.cursor().execute(f"INSERT INTO sentence (lang, text) VALUES ('{lang}', '{text}')")

    logging.info('Importing sentences from %s' % file_name)
    read_csv(file_name)
    logging.info('Finished')
    connection.commit()


options = get_arguments()
logging.basicConfig(format='[%(asctime)s %(levelname)s]: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level='INFO')
try:
    import_sentences(options.sentences)
except Exception as e:
    logging.error('Cannot import sentences: %s' % e)
    connection.rollback()
