import os
import datetime as dt

from flask import Flask, flash, get_flashed_messages,\
                  redirect, render_template, request,\
                  url_for
import validators

from .sql_manager import read_sql_urls, add_to_sql_urls,\
                         read_sql_url_checks, add_to_sql_url_checks


def get_today():
    return dt.datetime.now().date().strftime("%Y-%m-%d")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET')


@app.get('/')
def get_first():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/')
def add_url():
    URL = request.form.get('url')
    if not validators.url(URL):
        flash('Некорректный URL', 'error')
        return redirect(url_for('get_first'))

    # check if url is not already in DB
    for item in read_sql_urls():
        if URL == item['name']:
            flash('Страница уже существует', 'success')
            return redirect(url_for('show_one_url', id=item['id']))

    # the url to be added to DB
    add_to_sql_urls({'name': URL, 'created_at': get_today()})

    flash('Страница успешно добавлена', 'success')
    for item in read_sql_urls():
        if item['name'] == URL:
            entry = item
    return redirect(url_for('show_one_url', id=entry['id']))


@app.get('/urls')
def show_urls():
    messages = get_flashed_messages(with_categories=True)
    all_entries = read_sql_urls()
    return render_template('urls.html',
                           messages=messages,
                           all_entries=all_entries)


@app.get('/urls/<id>')
def show_one_url(id):
    # id to be pulled out of DB
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


@app.post('/urls/<id>/checks')
def check_url(id):
    # the url_check to be added to DB
    add_to_sql_url_checks({'url_id': int(id), 'created_at': get_today()})
    return redirect(url_for('show_one_url',  id=int(id)))
