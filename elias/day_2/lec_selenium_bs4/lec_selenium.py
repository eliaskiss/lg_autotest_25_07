from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import wget
import os
import sys
from icecream import ic
from webdriver_manager.chrome import ChromeDriverManager
import re

chrome_option = webdriver.ChromeOptions()

# chrome_option.add_argument('headless') # Hide Webbrowser
chrome_option.add_argument('window-size=1920x1080')
chrome_option.add_argument('disable-gpu')

# driver = webdriver.Chrome('chromedriver.exe', options=chrome_option)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=chrome_option))

# Selenium 4.6 버전이후
driver = webdriver.Chrome(options=chrome_option)

# 네이버 이동
driver.get('https://www.naver.com')

# 검색창 찾기
input_search = driver.find_element(By.ID, 'query')
# input_search = driver.find_element(By.NAME, 'query')
# input_search = driver.find_element(By.CLASS_NAME, 'search_input')
# input_search = driver.find_element(By.CSS_SELECTOR, '#query')           # '#' : ID
# input_search = driver.find_element(By.CSS_SELECTOR, '.search_input')    # '.' : Class Name

time.sleep(1)

# 검색어 입력
input_search.send_keys('네이버 영화')
time.sleep(1)

# 엔터키 입력
input_search.send_keys(Keys.ENTER)

# 영화카드를 담고 있는 박스
# card_area class = "card_area _panel"
card_area = driver.find_element(By.CSS_SELECTOR, '.card_area._panel')

# Total Page Count
total_page = driver.find_element(By.CSS_SELECTOR, '._total')
# total_page = driver.find_element(By.CLASS_NAME, '_total')
total_page = int(total_page.text)
ic(total_page)

# Next Page Button
next_link = driver.find_element(By.CSS_SELECTOR, '.pg_next.on._next')

for _ in range(total_page):
    time.sleep(1)
    movie_list = card_area.find_elements(By.CSS_SELECTOR, '.card_item')

    for movie in movie_list:
        try:
            ic('================================================================')
            # 영화 상세페이지 URL
            link = movie.find_element(By.CSS_SELECTOR, '.img_box')
            link = link.get_attribute('href')

            # 영화 고유코드번호 (Unique한 값)
            code = link.split('&os=')[1][:8]
            if '&' in code:
                code = code.replace('&', '')
            # code = re.sub('&', '', code)
            # code = re.findall('[0-9]+', code)[0]
            # code = re.findall('\d+', code)[0]
            # code = re.match('\d+', code)[0]

            # 영화포스터 이미지
            img = movie.find_element(By.TAG_NAME, 'img')
            # img = movie.find_element(By.CSS_SELECTOR, 'img')
            img_url = img.get_attribute('src')

            # Image 폴더 생성
            if os.path.exists('./images') is False:
                os.mkdir('images')

            # 포스터 이미지 다운로드
            wget.download(img_url, f'./images/{code}.jpg')

            # 큰 포스터 이미지 다운로드
            original_url = img_url.replace('304x456' , '800x1200')
            wget.download(original_url, f'./images/{code}_origin.jpg')

            # 영화제목
            title = movie.find_element(By.CSS_SELECTOR, '.area_text_box')
            title = title.text

            # 영화상세정보 목록
            info_list = movie.find_elements(By.CSS_SELECTOR, '.info_group')

            # 영화 장르, 상영시간
            # 개요\n스릴러\n180분 -> ['개요', '스릴러', '180분']
            _, category, running_time = info_list[0].text.split('\n')

            # 개봉일, 평점
            # 개봉\n2024.04.19\n평점\n7.7 -> ['개봉', '2024.04.19', '평점', '7.7']
            _, open_date, _, score = info_list[1].text.split('\n')

            # 출연배우
            # 출연\n어쩌구저쩌구...
            if len(info_list[2].text) != 0:
                _, actors = info_list[2].text.split('\n')
            else:
                actors = ''

            ic(title)
            ic(category)
            ic(running_time)
            ic(open_date)
            ic(score)
            ic(actors)
            ic(link)
            ic(img_url)
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    next_link.click()

















