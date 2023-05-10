import datetime as dt

from psycopg2.extras import DictCursor

SELECT_URL_BY_ID = """
SELECT * FROM urls WHERE urls.id = %(id)s
;
"""

SELECT_URL_BY_NAME = """
SELECT * FROM urls WHERE urls.name = %(name)s
;
"""

SELECT_URLS_AND_CHECKS = """
SELECT
  DISTINCT ON (urls.id)
    urls.id,
    urls.name,
    status_code,
    url_checks.created_at
FROM urls
LEFT JOIN
  url_checks
    ON urls.id = url_checks.url_id
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


def get_url_by_name(conn, name):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(SELECT_URL_BY_NAME, {'name': name})
        found_item = curs.fetchone()
    return found_item


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(SELECT_URL_BY_ID, {'id': id})
        found_item = curs.fetchone()
    return found_item


def get_urls(conn):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(SELECT_URLS_AND_CHECKS)
        all_entries = curs.fetchall()
    return all_entries


def add_to_urls(conn, values):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        values.update({'created_at': dt.datetime.now()})
        curs.execute(INSERT_URL, values)
        returned_id = curs.fetchone()['id']
    return returned_id


def get_url_checks(conn, url_id):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(SELECT_URL_CHECKS, url_id)
        all_entries = curs.fetchall()
    return all_entries


def add_to_url_checks(conn, values):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        values.update({'created_at': dt.datetime.now()})
        curs.execute(INSERT_URL_CHECKS, values)
