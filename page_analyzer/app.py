import os

from flask import Flask, flash, redirect, render_template, request, url_for
import validators
from urllib.parse import urlparse

from .sql_manager import read_sql_urls, add_to_sql_urls,\
                         read_sql_url_checks, add_to_sql_url_checks
from .http_requests import get_status, get_content


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET')


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

    # check if url is not already in DB
    for item in read_sql_urls():
        if url_for_check == item['name']:
            flash('Страница уже существует', 'success')
            return redirect(url_for('show_one_url', id=item['id']))

    # add the url to DB
    add_to_sql_urls({'name': url_for_check})
    flash('Страница успешно добавлена', 'success')
    for item in read_sql_urls():
        if item['name'] == url_for_check:
            entry = item
    return redirect(url_for('show_one_url', id=entry['id']))


# all urls - GET
@app.get('/urls')
def show_urls():
    # show all the urls that were added by users
    all_entries = read_sql_urls()
    return render_template('urls.html',
                           all_entries=all_entries)


# one url - GET
@app.get('/urls/<int:id>')
def show_one_url(id):
    # ID is pulled out of DB
    entry = {}
    for item in read_sql_urls():
        if item['id'] == id:
            entry = item
            entry_checks = read_sql_url_checks({'url_id': id})
    return render_template('one_url.html',
                           entry=entry,
                           entry_checks=entry_checks)


# check one url - POST
@app.post('/urls/<int:id>/checks')
def check_url(id):
    # the url check to be added to DB
    for item in read_sql_urls():
        if item['id'] == id:
            web_address = item['name']
    if get_status(web_address) == 404:
        flash('Произошла ошибка при проверке', 'error')
    else:
        flash('Страница успешно проверена', 'success')
        content = get_content(web_address)
        content.update({'url_id': id,
                        'status_code': get_status(web_address)})
        add_to_sql_url_checks(content)
    return redirect(url_for('show_one_url',  id=id))
