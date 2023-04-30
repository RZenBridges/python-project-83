
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
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_first'))
