import requests
from bs4 import BeautifulSoup as BS

URL = 'https://www.securitylab.ru/news/'

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
    items = soup.find_all('div', class_='article-card')
    news = []
    for item in items:
        news.append(
            dict(title=item.find('div', class_="article-card inline-card").get.Text(),
                 link=URL + items.find('a', class_='an').get('href'),
                 imag=URL + item.find('div', class_='iarticle-img').find('img').get('src'))
        )
    return news


def parser():
    html = ger_html(URL)
    if html.status_code == 200:
        news = []
        for page in range(0, 2):
            html = ger_html(f"{URL}latest/{page}")
            news.extend(get_data(html.text))
        return news


    else:
        raise Exception("Error in parser!")


print(parser())
