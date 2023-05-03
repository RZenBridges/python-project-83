import requests
from requests.exceptions import ConnectionError


def get_status(web_address):
    try:
        r = requests.get(web_address)
        return r.status_code
    except ConnectionError:
        return 404
