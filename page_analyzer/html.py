from bs4 import BeautifulSoup


def get_seo_content(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    description = ''
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    metatags = soup.find_all('meta', attrs={'name': 'description'})
    for tag in metatags:
        description = tag.get('content')
    return {'h1': h1, 'title': title, 'description': description}
