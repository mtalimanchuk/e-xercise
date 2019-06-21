#!/usr/bin/python3

import logging

import pymysql


class ClassroomDb:
    def __init__(self, db_host, username, password, db_name):
        if db_host is None or username is None or password is None or db_name is None:
            raise Exception(
                "Database connection properties cannot be blank. URL, username, password and db name are mandatory.")
        self.db_host = db_host
        self.username = username
        self.password = password
        self.db_name = db_name
        self.connection = pymysql.connect(self.db_host, self.username, self.password, self.db_name)
        self.connection.autocommit(False)

    def query_for_object(self, query):
        if query is None or query == '':
            raise Exception("SQL query cannot be blank")
        if 'UPDATE' in query.upper() or 'DELETE' in query.upper() or 'DELETE' in query.upper():
            raise Exception("Illegal statement provided in query. Only SELECT is allowed.")
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchone()
            cursor.close()
            return "%s" % data
        except pymysql.err.ProgrammingError as mysqlError:
            logging.error(f"SQL syntax error: {mysqlError}")
        except Exception as e:
            logging.error(f'Unexpected error during SQL execution: {e}')

    def query_for_list(self, query):
        if query is None or query == '':
            raise Exception("SQL query cannot be blank")
        if 'UPDATE' in query.upper() or 'DELETE' in query.upper() or 'DELETE' in query.upper():
            raise Exception("Illegal statement provided in query. Only SELECT is allowed.")
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return "%s" % data
        except pymysql.err.ProgrammingError as mysqlError:
            logging.error(f"SQL syntax error: {mysqlError}")
            return
        except Exception as e:
            logging.error(f'Unexpected error during SQL execution: {e}')
            return

    def execute_statement(self, statement):
        if statement is None or statement == '':
            raise Exception("SQL statement cannot be blank.")
        try:
            logging.debug('Executing: %s' % statement)
            cursor = self.connection.cursor()
            cursor.execute(statement)
            self.connection.commit()
            cursor.close()
            return True
        except pymysql.err.ProgrammingError as mysqlError:
            logging.error(f'SQL syntax error: {mysqlError}')
            self.connection.rollback()
        except Exception as e:
            logging.error(f'SQL execution failed: {e}')
            self.connection.rollback()

    def execute_statements(self, list_of_statements):
        if list_of_statements is None or len(list_of_statements) == 0:
            raise Exception("List of SQL statements cannot be empty.")
        try:
            logging.debug('Batch execution: %s' % list_of_statements)
            cursor = self.connection.cursor()
            for q in list_of_statements.split(";"):
                if q is None or q == '' or q == '#' or q == ';':
                    continue
                logging.debug('Executing: %s', q)
                cursor.execute(q)
            self.connection.commit()
            cursor.close()
            return True
        except pymysql.err.ProgrammingError as pymysql_error:
            logging.error(f'Database syntax error: {pymysql_error}')
            self.connection.rollback()
        except Exception as e:
            logging.error(f'SQL execution failed: {e}')
            self.connection.rollback()

    def init_schema(self, schema_init_file):
        if schema_init_file is None or schema_init_file == '':
            raise Exception("Schema creation file cannot be blank")
        initialized = self.execute_statements(open(schema_init_file, 'r').read().replace('\n', ' '))
        if initialized:
            logging.info('Schema initialized.')
        else:
            logging.warning('Schema was not initialized')

    def init_test_data(self, test_data_file):
        if test_data_file is None or test_data_file == '':
            raise Exception("Test data creation file cannot be blank")
        initialized = self.execute_statements(open(test_data_file, 'r').read().replace('\n', ' '))
        if initialized:
            logging.info('Test data have been inserted.')
        else:
            logging.warning('Test data was not inserted.')
