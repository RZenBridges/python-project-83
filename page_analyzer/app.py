import os
import datetime as dt

from flask import Flask, flash, get_flashed_messages,\
                  redirect, render_template, request,\
                  url_for
import validators
from urllib.parse import urlparse

from .sql_manager import read_sql_urls, add_to_sql_urls,\
                         read_sql_url_checks, add_to_sql_url_checks
from .http_requests import get_status, get_content


def get_today():
    return dt.datetime.now().date().strftime("%Y-%m-%d")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET')


# main page - GET
@app.get('/')
def get_first():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


# main page - POST
@app.post('/')
def add_url():
    # url from the form is processed
    url_for_check = '://'.join(
        list(
            urlparse(
                request.form.get('url').lower()
            )
        )[:2]
    )
    # check if url has a correct features
    if not validators.url(url_for_check):
        flash('Некорректный URL', 'error')
        return redirect(url_for('get_first'))

    # check if url is not already in DB
    for item in read_sql_urls():
        if url_for_check == item['name']:
            flash('Страница уже существует', 'success')
            return redirect(url_for('show_one_url', id=item['id']))

    # add the url to DB
    add_to_sql_urls({'name': url_for_check, 'created_at': get_today()})
    flash('Страница успешно добавлена', 'success')
    for item in read_sql_urls():
        if item['name'] == url_for_check:
            entry = item
    return redirect(url_for('show_one_url', id=entry['id']))


# all urls - GET
@app.get('/urls')
def show_urls():
    # show all the urls that were added by users
    messages = get_flashed_messages(with_categories=True)
    all_entries = read_sql_urls()
    return render_template('urls.html',
                           messages=messages,
                           all_entries=all_entries)


# one url - GET
@app.get('/urls/<id>')
def show_one_url(id):
    # ID is pulled out of DB
    entry = {}
    for item in read_sql_urls():
        if item['id'] == int(id):
            entry = item
            entry_checks = read_sql_url_checks({'url_id': int(id)})
    messages = get_flashed_messages(with_categories=True)
    return render_template('one_url.html',
                           messages=messages,
                           entry=entry,
                           entry_checks=entry_checks)


# check one url - POST
@app.post('/urls/<id>/checks')
def check_url(id):
    # the url check to be added to DB
    for item in read_sql_urls():
        if item['id'] == int(id):
            web_address = item['name']
    if get_status(web_address) == 404:
        flash('Произошла ошибка при проверке', 'error')
    else:
        flash('Страница успешно проверена', 'success')
        content = get_content(web_address)
        content.update({'url_id': int(id),
                        'created_at': get_today(),
                        'status_code': get_status(web_address)})
        add_to_sql_url_checks(content)
    return redirect(url_for('show_one_url',  id=int(id)))
