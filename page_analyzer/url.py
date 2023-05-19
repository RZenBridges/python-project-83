import validators
from urllib.parse import urlparse


def normalize(inserted_url):
    lower_url = inserted_url.lower()
    url_parts = urlparse(lower_url)
    if url_parts.scheme and url_parts.netloc:
        url_for_check = f'{url_parts.scheme}://{url_parts.netloc}'
    else:
        url_for_check = lower_url
    return url_for_check


def validate(url_for_check):
    alert = []
    if url_for_check == '':
        alert.append('URL обязателен')
    if len(url_for_check) > 255:
        alert.append('URL не может превышать 255 символов')
    if not validators.url(url_for_check):
        alert.append('Некорректный URL')
    return alert
