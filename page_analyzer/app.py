import os
import requests
from requests.exceptions import RequestException
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
import psycopg2

from .database import get_urls, add_to_urls, get_url_checks,\
    add_to_url_checks, get_url_by_name, get_url_by_id
from .html import get_seo_content
from .url import normalize, validate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret_key')
DATABASE_URL = os.environ.get('DATABASE_URL')


@app.errorhandler(404)
def not_found(error):
    return '<h1>Страница не существует</h1>', 404


# main page - GET
@app.get('/')
def index():
    return render_template('index.html')


# main page - POST
@app.post('/urls')
def add_url():
    # check if the url from the form is correct
    queried_url = request.form.get('url')
    is_normal, normal_url = normalize(queried_url)
    is_valid, valid_url = validate(normal_url)
    if not all([is_normal, is_valid]):
        for status, message in ((is_normal, normal_url), (is_valid, valid_url)):
            flash(message, 'error') if status is False else None
        return render_template('index.html', user_input=queried_url), 422

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            item = get_url_by_name(conn, name=valid_url)
            if item:
                id = item['id']
                flash('Страница уже существует', 'success')
            else:
                id = add_to_urls(conn, valid_url)
                flash('Страница успешно добавлена', 'success')
    finally:
        conn.close()
    return redirect(url_for('show_url', id=id))


# all urls - GET
@app.get('/urls')
def show_urls():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            all_urls = get_urls(conn)
    finally:
        conn.close()
    return render_template('urls.html', all_entries=all_urls)


# one url - GET
@app.get('/urls/<int:id>')
def show_url(id):
    conn = psycopg2.connect(DATABASE_URL)
    # ID is pulled out of DB
    try:
        item = get_url_by_id(conn, id=id)
        if item:
            url_checks = get_url_checks(conn, {'url_id': item['id']})
        else:
            flash('Такой страницы не существует', 'error')
            return redirect(url_for('index'))
    finally:
        conn.close()

    return render_template('one_url.html', url=item, url_checks=url_checks)


# check one url - POST
@app.post('/urls/<int:id>/checks')
def check_url(id):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            item = get_url_by_id(conn, id=id)
            if item:
                url = item['name']
            else:
                return '', 404
            try:
                response = requests.get(url)
                response.raise_for_status()
                h1, title, description = get_seo_content(response.text)
                add_to_url_checks(conn,
                                  url_id=id,
                                  status_code=response.status_code,
                                  h1=h1,
                                  title=title,
                                  description=description)
                flash('Страница успешно проверена', 'success')
            except RequestException:
                flash('Произошла ошибка при проверке', 'error')
    finally:
        conn.close()
    return redirect(url_for('show_url', id=id))
