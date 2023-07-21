import csv
import datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import streamlit as st

def extract_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 본문 추출
    content_element = soup.select_one('#snsAnchor > div')
    if content_element is None:
        raise ValueError("Could not find article content")
    content = "\n".join([p.get_text() for p in content_element.find_all('p')])

    return content

def extract_article_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles_data = []

    article_elements = soup.select('#section-list > ul > li')
    for article_element in article_elements:
        title = article_element.select_one('div > h4 > a').text
        link = urljoin(url, article_element.select_one('div > h4 > a')['href'])

        date_text = article_element.select_one('div > span > em').text
        date_text = date_text.replace("입력 ", "")
        date = datetime.datetime.strptime(date_text, '%Y.%m.%d %H:%M')
        date_str = date.strftime('%Y-%m-%d-%H-%M')

        tag = article_element.select_one('div > span > em:nth-child(1)').text

        content = extract_article_content(link)

        articles_data.append([date_str, title, content, link, tag])

    return articles_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Title", "Content", "Link", "Tag"])
        writer.writerows(data)

# Streamlit layout
st.title('WB_ArticleScraper')

# URL 선택 옵션
option = st.selectbox('URL 입력 방식', ['인공지능신문(aitimes) AI 산업군 - 제목형', '직접 입력'])

if option == '인공지능신문(aitimes) AI 산업군 - 제목형':
    url = "https://www.aitimes.kr/news/articleList.html?page=1&total=3382&sc_section_code=S1N4&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&box_idxno=&sc_multi_code=&sc_is_image=&sc_is_movie=&sc_user_name=&sc_order_by=E"
else:
    url = st.text_input("뉴스 기사 리스트 URL을 입력하세요: ", "")

if url:
    try:
        # Adjust URL to include https:// if not present
        if not url.startswith('https://'):
            if url.startswith('www.'):
                url = "https://" + url  # 스키마 추가
            else:
                url = "https://www." + url  # 스키마 추가
        articles_data = extract_article_list(url)
        save_to_csv(articles_data, 'articles.csv')
        st.success('Articles saved to articles.csv')
    except Exception as e:
        st.error(f"An error occurred: {e}")
