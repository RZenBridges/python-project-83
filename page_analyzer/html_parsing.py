from bs4 import BeautifulSoup


def get_content(parsed_html):
    soup = BeautifulSoup(parsed_html.text, 'html.parser')
    h1, title, description = '', '', ''
    if soup.h1:
        h1 = soup.h1.text
    if soup.title:
        title = soup.title.text
    metatags = soup.find_all('meta', attrs={'name': 'description'})
    for tag in metatags:
        description = tag.get('content')
    return {'h1': h1, 'title': title, 'description': description}
