import os
import datetime as dt

from flask import Flask, flash, get_flashed_messages,\
                  redirect, render_template, request,\
                  url_for
import validators

from .sql_manager import read_sql, add_to_sql


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
    for item in read_sql():
        if URL == item['name']:
            flash('Страница уже существует', 'success')
            return redirect(url_for('show_one_url', id=item['id']))

    # the url to be added to DB
    add_to_sql({'name': URL, 'created_at': get_today()})

    flash('Страница успешно добавлена', 'success')
    for item in read_sql():
        if item['name'] == URL:
            entry = item
    return redirect(url_for('show_one_url', id=entry['id']))


@app.get('/urls')
def show_urls():
    messages = get_flashed_messages(with_categories=True)
    all_entries = read_sql()
    return render_template('urls.html',
                           messages=messages,
                           all_entries=all_entries)


@app.get('/urls/<id>')
def show_one_url(id):
    # id to be pulled out of DB
    entry = {}
    for item in read_sql():
        if item['id'] == int(id):
            entry = item
    messages = get_flashed_messages(with_categories=True)
    return render_template('one_url.html', messages=messages, entry=entry)


@app.post('/urls/<id>')
def analyze_website(id):
    # id to be pulled out of DB
    return redirect(url_for('show_one_url', id=1))
