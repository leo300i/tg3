import requests
from bs4 import BeautifulSoup as BS

URL = 'https://animekisa.tv/'

HEADERS = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    "USER_name": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/100.0.4896.127 Safari/537.36 "
}


def ger_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_data(html):
    soup = BS(html, "html.parser")
    items = soup.find_all('div', class_='episode-box test')
    anime = []
    for item in items:
        anime.append(
            {
                "title": item.find('div', class_="title-box-2").getText(),
                'link': URL + items.find('a', class_='an').get('href'),
                'imag': URL + item.find('div', class_='image-box').find('img').get('src')
            }
        )
    return anime


def parser():
    html = ger_html(URL)
    if html.status_code == 200:
        anime = []
        for page in range(0, 3):
            html = ger_html(f"{URL}latest/{page}")
            anime.extend(get_data(html.text))
        return anime


    else:
        raise Exception("Error in parser!")