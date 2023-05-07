import os
import datetime as dt

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

SELECT_URL_BY_ID = """
SELECT * FROM urls WHERE urls.id = %(id)s
"""

SELECT_URL_BY_NAME = """
SELECT * FROM urls WHERE urls.name = %(name)s
"""

SELECT_URLS_AND_CHECKS = """
SELECT
  DISTINCT ON (urls.id)
    urls.id,
    urls.name,
    status_code,
    url_checks.created_at AS check_made_at
FROM urls
LEFT JOIN
  url_checks
    ON urls.id = url_checks.url_id
GROUP BY
    urls.id,
    url_checks.id,
    status_code
ORDER BY
    urls.id,
    url_checks.id DESC
;
"""

INSERT_URL = """
INSERT INTO urls (name, created_at)
VALUES (%(name)s, %(created_at)s)
RETURNING id
;
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


def read_sql_urls_by_name(name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(SELECT_URL_BY_NAME, {'name': name})
            found_item = curs.fetchone()
        return found_item


def read_sql_urls_by_id(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(SELECT_URL_BY_ID, {'id': id})
            found_item = curs.fetchone()
        return found_item


def read_sql_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(SELECT_URLS_AND_CHECKS)
            all_entries = curs.fetchall()
        return all_entries


def add_to_sql_urls(values):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            values.update({'created_at': dt.datetime.now().date()})
            curs.execute(INSERT_URL, values)
            returned_id = curs.fetchone()['id']
        conn.commit()
    return returned_id


def read_sql_url_checks(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(SELECT_URL_CHECKS, url_id)
            all_entries = curs.fetchall()
        return all_entries


def add_to_sql_url_checks(values):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            values.update({'created_at': dt.datetime.now().date()})
            curs.execute(INSERT_URL_CHECKS, values)
        conn.commit()
