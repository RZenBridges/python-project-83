from bs4 import BeautifulSoup


def get_seo_content(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag.get('content') if description_tag else ''
    return h1, title, description
