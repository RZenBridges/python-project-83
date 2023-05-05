import os
import datetime as dt

import psycopg2
from psycopg2.extras import DictCursor

DATABASE_URL = os.environ.get('DATABASE_URL')

SELECT_URL = """
SELECT
    urls.*,
    status_code,
    MAX(url_checks.created_at) AS check_made_at
FROM urls
LEFT JOIN url_checks ON urls.id = url_checks.url_id
GROUP BY urls.id, status_code;
"""

INSERT_URL = """
INSERT INTO urls (name, created_at)
VALUES (%(name)s, %(created_at)s
);
"""

SELECT_URL_CHECKS = "SELECT * FROM url_checks WHERE url_id = (%(url_id)s);"
INSERT_URL_CHECKS = """
INSERT INTO url_checks (
    url_id,
    status_code,
    h1,
    title,
    description,
    created_at
)
VALUES (
    %(url_id)s,
    %(status_code)s,
    %(h1)s,
    %(title)s,
    %(description)s,
    %(created_at)s
);
"""


def read_sql_urls():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(SELECT_URL)
                all_entries = curs.fetchall()
            return all_entries
    except psycopg2.Error:
        print('Can`t establish connection to database')


def add_to_sql_urls(values):
    try:
        with psycopg2.conenct(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                values.update({'created_at': str(dt.datetime.now().date())})
                curs.execute(INSERT_URL, values)
            conn.commit()
    except psycopg2.Error:
        print('Can`t establish connection to database')


def read_sql_url_checks(url_id):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                curs.execute(SELECT_URL_CHECKS, url_id)
                all_entries = curs.fetchall()
            return all_entries
    except psycopg2.Error:
        print('Can`t establish connection to database')


def add_to_sql_url_checks(values):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=DictCursor) as curs:
                values.update({'created_at': str(dt.datetime.now().date())})
                curs.execute(INSERT_URL_CHECKS, values)
            conn.commit()
    except psycopg2.Error:
        print('Can`t establish connection to database')
