import os

from flask import Flask, flash, redirect, render_template, request, url_for
import validators
from urllib.parse import urlparse
from dotenv import load_dotenv
import psycopg2

from .database import get_urls, add_to_urls, get_url_checks,\
    add_to_url_checks, get_url_by_id, get_url_by_name
from .http_requests import get_status, get_content

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret_key')
DATABASE_URL = os.environ.get('DATABASE_URL')


# main page - GET
@app.get('/')
def get_first():
    return render_template('index.html')


# main page - POST
@app.post('/urls')
def add_url():
    # url from the form is processed
    raw_request = request.form.get('url')
    url = urlparse(raw_request.lower())
    url_for_check = f'{url.scheme}://{url.netloc}'
    # check if url has a correct features
    if not validators.url(url_for_check):
        flash('Некорректный URL', 'error')
        if raw_request == '':
            flash('URL обязателен', 'error')
        return render_template('index.html', user_input=raw_request), 422

    with psycopg2.connect(DATABASE_URL) as conn:
        # check if url is not already in DB
        item = get_url_by_name(conn, url_for_check)
        if item:
            flash('Страница уже существует', 'success')
            return redirect(url_for('show_one_url', id=item['id']))

        # add the url toflash('Страница успешно проверена', 'success')
        returned_id = add_to_urls(conn, {'name': url_for_check})
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_one_url', id=returned_id))


# all urls - GET
@app.get('/urls')
def show_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        # show all the urls that were added by users
        all_entries = get_urls(conn)
    return render_template('urls.html',
                           all_entries=all_entries)


# one url - GET
@app.get('/urls/<int:id>')
def show_one_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        # ID is pulled out of DB
        item = get_url_by_id(conn, id)
        entry_checks = get_url_checks(conn, {'url_id': item['id']})
        return render_template('one_url.html',
                               entry=item,
                               entry_checks=entry_checks)


# check one url - POST
@app.post('/urls/<int:id>/checks')
def check_url(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        # the url check to be added to DB
        item = get_url_by_id(conn, id)
        web_address = item['name']
        if get_status(web_address) == 404:
            flash('Произошла ошибка при проверке', 'error')
        else:
            content = get_content(web_address)
            content.update({'url_id': id,
                            'status_code': get_status(web_address)})
            add_to_url_checks(conn, content)
            flash('Страница успешно проверена', 'success')
        return redirect(url_for('show_one_url', id=id))
