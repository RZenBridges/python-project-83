from bs4 import BeautifulSoup


def get_seo_content(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    description = ''
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    metatag = soup.find('meta', attrs={'name': 'description'})
    description = metatag.get('content')
    return h1, title, description
