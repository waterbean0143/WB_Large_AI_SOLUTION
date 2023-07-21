import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_article_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_elements = soup.select('#section-list > ul > li')

    data = []
    for article in article_elements:
        title = article.select_one('div > h4 > a').get('target')
        link = urljoin(url, article.select_one('div > h4 > a').get('href'))
        tag = article.select_one('div > span > em:nth-child(1)').text
        date = article.select_one('div > span > em:nth-child(3)').text

        response = requests.get(link)
        article_soup = BeautifulSoup(response.content, 'html.parser')
        content = article_soup.select_one('#snsAnchor > div').text.strip()

        data.append([date, title, content, link, tag])

    return data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Title', 'Content', 'Link', 'Tag'])
        writer.writerows(data)

url = 'https://www.aitimes.kr/news/articleList.html?page=2&total=3388&sc_section_code=S1N4&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&box_idxno=&sc_multi_code=&sc_is_image=&sc_is_movie=&sc_user_name=&sc_order_by=E&view_type=sm'
data = extract_article_list(url)
save_to_csv(data, 'articles.csv')
