from bs4 import BeautifulSoup

def strip_tags(html):
    return BeautifulSoup(html).get_text()
