import os

import psycopg2
from psycopg2.extras import DictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

SELECT = "SELECT * FROM urls;"
INSERT = """
INSERT INTO urls (name, created_at)
VALUES (%(name)s, %(created_at)s);
"""


def read_sql():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(SELECT)
            all_entries = curs.fetchall()
            conn.close()
            return all_entries
    except:
        print('Can`t establish connection to database')


def add_to_sql(values):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print('DB connection established')
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(INSERT, values)
        conn.commit()
        conn.close()
        return True
    except:
        print('Can`t establish connection to database')
        return False
