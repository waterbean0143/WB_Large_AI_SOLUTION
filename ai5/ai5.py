import csv
import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime

def extract_article_list(url):
    # 1. URL에서 HTML 내용 가져오기
    response = requests.get(url)
    html_content = response.content

    # 2. HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 3. 기사 제목 추출
    article_titles = []
    title_elements = soup.select('#section-list > ul > li > h4.titles')
    for title_element in title_elements:
        article_title = title_element.get_text()
        article_titles.append(article_title)

    # 4. 기사 링크 추출
    article_links = []
    link_elements = soup.select('#section-list > ul > li > h4 > a')
    for link_element in link_elements:
        article_link = link_element.get('href')
        article_url = urljoin(url, article_link)  # 절대 경로로 변환
        article_links.append(article_url)

    # 5. 기사 본문, 시간, 태그 추출
    article_contents = []
    article_times = []
    article_tags = []
    for link in article_links:
        article_content, article_time, article_tag = extract_article_content(link)
        article_contents.append(article_content)
        article_times.append(article_time)
        article_tags.append(article_tag)

    return article_titles, article_links, article_contents, article_times, article_tags

def extract_article_content(url):
    # 1. URL에서 HTML 내용 가져오기
    response = requests.get(url)
    html_content = response.content

    # 2. HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 3. 본문 추출
    article_content_element = soup.select_one('#snsAnchor > div')
    if article_content_element is None:
        raise ValueError("Could not find article content")
    article_content_paragraphs = article_content_element.find_all('p')
    article_content = "\n".join([p.get_text() for p in article_content_paragraphs])

    # 4. 시간 추출
    article_time_element = soup.select_one('#article-view > div > header > div > article:nth-child(1) > ul > li:nth-child(2) > i')
    article_time = article_time_element.text if article_time_element else "<na>"
    if article_time != "<na>":
        publish_time = datetime.strptime(article_time[3:], '%Y.%m.%d %H:%M')
        article_time = datetime.strftime(publish_time, '%Y-%m-%d-%H-%M')
    
    # 5. 태그 추출
    article_tag_element = soup.select_one('#article-view > div > header > nav > ul > li:nth-child(3) > a')
    article_tag = article_tag_element.text if article_tag_element else "<na>"

    return article_content, article_time, article_tag

def save_to_csv(titles, links, contents, times, tags, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Title", "Content", "Link", "Tag"])
        for time, title, content, link, tag in zip(times, titles, contents, links, tags):
            writer.writerow([time, title, content, link, tag])

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
        article_titles, article_links, article_contents, article_times, article_tags = extract_article_list(url)
        save_to_csv(article_titles, article_links, article_contents, article_times, article_tags, 'articles.csv')
        st.success('Articles saved to articles.csv')

        # Load the CSV data into a pandas DataFrame
        articles_df = pd.read_csv('articles.csv')

        # Display the DataFrame in the Streamlit app
        st.dataframe(articles_df)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
