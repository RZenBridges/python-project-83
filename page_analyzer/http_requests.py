import requests
from requests.exceptions import ConnectionError

from bs4 import BeautifulSoup

def get_status(web_address):
    try:
        r = requests.get(web_address)
        return r.status_code
    except ConnectionError:
        return 404


def get_content(web_address):
    r = requests.get(web_address)
    soup = BeautifulSoup(r.text, 'html.parser')
    h1, title, description = '', '', ''
    if soup.h1:
        h1 = soup.h1.text
    if soup.title:
        title = soup.title.text
    if soup.head and soup.head.meta:
        for item in soup.head.find_all('meta'):
            if item.get('name') == 'description' and item.get('content'):
                description = item['content']
    return {'h1': h1, 'title': title, 'description': description}
