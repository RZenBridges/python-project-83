import validators
from urllib.parse import urlparse


def normalize(inserted_url):
    if inserted_url == '':
        return False, 'URL обязателен'
    url_parts = urlparse(inserted_url.lower())
    url_for_check = f'{url_parts.scheme}://{url_parts.netloc}'
    return True, url_for_check


def validate(url_for_check):
    if len(url_for_check) > 255:
        return False, 'URL не может превышать 255 символов'
    if not validators.url(url_for_check):
        return False, 'Некорректный URL'
    return True, url_for_check
