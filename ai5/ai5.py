import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import streamlit as st
import datetime

def extract_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 본문 추출
    content_element = soup.select_one('#snsAnchor > div')
    if content_element is None:
        raise ValueError("Could not find article content")
    content = "\n".join([p.get_text() for p in content_element.find_all('p')])

    # 시간 추출 및 형식 변환
    time = soup.select_one('#article-view > div > header > div > article:nth-child(1) > ul > li:nth-child(2) > i').text
    time = time.replace("입력 ", "")  # '입력 ' 삭제
    time = datetime.datetime.strptime(time, '%Y.%m.%d %H:%M')  # 시간 형식 지정
    time = time.strftime('%Y-%m-%d-%H-%M')  # 출력 형식 지정

    # 태그 추출
    tag = soup.select_one('#article-view > div > header > nav > ul > li:nth-child(3) > a').text

    return content, time, tag

def extract_article_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    links = []
    dates = []
    tags = []
    contents = []

    # Assuming there are 20 articles per page
    for i in range(1, 21):
        title = soup.select_one(f'#section-list > ul > li:nth-child({i}) > div > h4 > a').get('target')
        link = urljoin(url, soup.select_one(f'#section-list > ul > li:nth-child({i}) > div > h4 > a').get('href'))
        date = soup.select_one(f'#section-list > ul > li:nth-child({i}) > div > span > em:nth-child(3)').text
        tag = soup.select_one(f'#section-list > ul > li:nth-child({i}) > div > span > em:nth-child(1)').text

        content, time, tag = extract_article_content(link)

        titles.append(title)
        links.append(link)
        dates.append(date)
        tags.append(tag)
        contents.append(content)

    return titles, links, dates, tags, contents

def save_to_csv(titles, links, dates, tags, contents, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Title", "Content", "Link", "Tag"])
        for date, title, content, link, tag in zip(dates, titles, contents, links, tags):
            writer.writerow([date, title, content, link, tag])

st.title('WB_ArticleScraper')

url = "https://www.aitimes.kr/news/articleList.html?page=1&total=3382&sc_section_code=S1N4&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&box_idxno=&sc_multi_code=&sc_is_image=&sc_is_movie=&sc_user_name=&sc_order_by=E&view_type=sm"

try:
    titles, links, dates, tags, contents = extract_article_list(url)
    save_to_csv(titles, links, dates, tags, contents, 'articles.csv')
    st.success('Articles saved to articles.csv')
    df = pd.read_csv('articles.csv')
    st.write(df)
except Exception as e:
    st.error(f"An error occurred: {e}")
