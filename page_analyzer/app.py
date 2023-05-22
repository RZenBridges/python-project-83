import os
import logging
import requests
from requests.exceptions import RequestException

from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv

from .database import get_urls, add_to_urls, get_url_checks,\
    add_to_url_checks, get_url_by_name, get_url_by_id, connection
from .html import get_seo_content
from .url import normalize, validate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET', 'secret_key')
DATABASE_URL = os.environ.get('DATABASE_URL')


@app.errorhandler(404)
def not_found(error):
    return '<h1>Страница не существует 404</h1>', 404


@app.errorhandler(500)
def server_error(error):
    return '<h1>Страница не существует 500</h1>', 404


# main page - GET
@app.get('/')
def index():
    return render_template('index.html')


# main page - POST
@app.post('/urls')
def add_url():
    # check if the url from the form is correct
    url = request.form.get('url')
    normalized_url = normalize(url)
    warning = validate(normalized_url)
    if warning:
        flash(warning, 'error')
        return render_template('index.html', user_input=url), 422

    with connection(DATABASE_URL) as conn:
        found_url = get_url_by_name(conn, normalized_url)
        if found_url:
            id = found_url['id']
            flash('Страница уже существует', 'success')
        else:
            id = add_to_urls(conn, normalized_url)
            flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=id))


# all urls - GET
@app.get('/urls')
def show_urls():
    with connection(DATABASE_URL) as conn:
        all_urls = get_urls(conn)
    return render_template('urls.html', all_entries=all_urls)


# one url - GET
@app.get('/urls/<int:id>')
def show_url(id):
    with connection(DATABASE_URL) as conn:
        # ID is pulled out of DB
        found_url = get_url_by_id(conn, id)
        if not found_url:
            flash('Такой страницы не существует', 'error')
            return redirect(url_for('index'))
        url_checks = get_url_checks(conn, {'url_id': found_url['id']})
    return render_template('one_url.html', url=found_url, url_checks=url_checks)


# check one url - POST
@app.post('/urls/<int:id>/checks')
def check_url(id):
    with connection(DATABASE_URL) as conn:
        found_url = get_url_by_id(conn, id)
        try:
            response = requests.get(found_url['name'])
            response.raise_for_status()
        except (RequestException, TypeError):
            logging.error(f"No url is registered under the id {id}")
            flash('Произошла ошибка при проверке', 'error')
        else:
            h1, title, description = get_seo_content(response.text)
            add_to_url_checks(conn,
                              url_id=id,
                              status_code=response.status_code,
                              h1=h1,
                              title=title,
                              description=description)
            flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id))
