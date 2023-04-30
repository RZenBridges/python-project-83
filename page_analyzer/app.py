
from flask import Flask, flash, get_flashed_messages,\
                  redirect, render_template, request,\
                  url_for
import validators

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


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
    # the url to be added to DB
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_one_url', id=1))


@app.get('/urls')
def show_urls():
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls.html', messages=messages)


@app.get('/urls/<id>')
def show_one_url(id):
    # id to be pulled out of DB
    messages = get_flashed_messages(with_categories=True)
    return render_template('one_url.html', messages=messages)


@app.post('/urls/<id>')
def analyze_website(id):
    # id to be pulled out of DB
    return redirect(url_for('show_one_url', id=1))
