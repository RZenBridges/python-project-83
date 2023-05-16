import datetime as dt

from psycopg2.extras import DictCursor

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
    url_checks.created_at DESC;
"""

INSERT_URL = """
INSERT INTO urls (name, created_at)
VALUES (%s, %s)
RETURNING id;
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


def get_url_by(conn, **kwargs):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        key = list(kwargs.keys())[0]
        curs.execute(f"SELECT * FROM urls WHERE urls.{key} = %({key})s;",
                     kwargs)
        found_item = curs.fetchone()
    return found_item


# сохранил DictCursor поскольку кажется, что в таком виде в html
# элементы раскрываются явно через имена id, title и тд
# разве так не лучше?
def get_urls(conn):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(SELECT_URLS_AND_CHECKS)
        all_entries = curs.fetchall()
    return all_entries


def add_to_urls(conn, url):
    with conn.cursor() as curs:
        curs.execute(INSERT_URL, (url, dt.datetime.now()))
        returned_id, = curs.fetchone()
    return returned_id


# сохранил DictCursor поскольку кажется, что в таком виде в html
# элементы раскрываются явно через имена id, title и тд
# разве так не лучше?
def get_url_checks(conn, url_id):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(SELECT_URL_CHECKS, url_id)
        all_entries = curs.fetchall()
    return all_entries


def add_to_url_checks(conn, **kwargs):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(INSERT_URL_CHECKS,
                     kwargs | {'created_at': dt.datetime.now()})
