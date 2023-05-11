import os
import requests
from requests.exceptions import RequestException

from flask import Flask, flash, redirect, render_template, request, url_for
import validators
from urllib.parse import urlparse
from dotenv import load_dotenv
import psycopg2

from .database import get_urls, add_to_urls, get_url_checks,\
    add_to_url_checks, get_url_by
from .html_parsing import get_content

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret_key')
DATABASE_URL = os.environ.get('DATABASE_URL')


# main page - GET
@app.get('/')
def index():
    return render_template('index.html')


# main page - POST
@app.post('/urls')
def add_url():
    # url from the form is processed
    user_input = request.form.get('url')
    if user_input == '':
        flash('URL обязателен', 'error')
    url_parts = urlparse(user_input.lower())
    url_for_check = f'{url_parts.scheme}://{url_parts.netloc}'
    # check if url has correct features
    if not validators.url(url_for_check) or len(url_for_check) > 255:
        flash('Некорректный URL', 'error')
        return render_template('index.html', user_input=user_input), 422

    with psycopg2.connect(DATABASE_URL) as conn:
        item = get_url_by(conn, url_for_check)
        if item:
            id = item['id']
            flash('Страница уже существует', 'success')
        else:
            id = add_to_urls(conn, {'name': url_for_check})
            flash('Страница успешно добавлена', 'success')
    conn.close()
    return redirect(url_for('show_one_url', id=id))


# all urls - GET
@app.get('/urls')
def show_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        all_urls = get_urls(conn)
    conn.close()
    return render_template('urls.html',
                           all_entries=all_urls)


# one url - GET
@app.get('/urls/<int:id>')
def show_one_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        # ID is pulled out of DB
        item = get_url_by(conn, id)
        try:
            url_checks = get_url_checks(conn, {'url_id': item['id']})
        except TypeError:
            flash('Такой страницы не существует', 'error')
    conn.close()
    if item is None:
        return redirect(url_for('index'))
    return render_template('one_url.html',
                           entry=item,
                           entry_checks=url_checks)


# check one url - POST
@app.post('/urls/<int:id>/checks')
def check_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        item = get_url_by(conn, id)
        url = item['name']
        try:
            r = requests.get(url)
            r.raise_for_status()
            content = get_content(r)
            content.update({'url_id': id,
                            'status_code': r.status_code})
            add_to_url_checks(conn, content)
            flash('Страница успешно проверена', 'success')
        except RequestException:
            flash('Произошла ошибка при проверке', 'error')
    conn.close()
    return redirect(url_for('show_one_url', id=id))
