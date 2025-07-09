from bs4 import BeautifulSoup as bs
import wget
import os
from icecream import ic
import requests

req = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EC%98%81%ED%99%94&oquery=%EB%84%A4%EC%9D%B4%EB%B2%84+%EC%98%81%ED%99%94&tqi=iMO73lp0J14ssdaumLVssssstiw-342447')
html = req.text

header = req.headers
for key in header.keys():
    print('Header:', key)
    print('Value:', header[key])
    print('-' * 20)

status = req.status_code
print('Status:', status)

soup = bs(html, 'html.parser')

# 네이버 영화링크
current_move_link = soup.find(class_='card_area _panel')
movie_list = current_move_link.findChildren('div', class_='card_item')

for movie in movie_list:
    try:
        ic('===========================================================================')
        # 영화 상세페이지
        link = movie.find('a', class_='img_box')
        link = link['href']

        # 영화 고유코드
        code = link.split('&os=')[1][:8]
        if '&' in code:
            code = code.replace('&', '')
        # code = re.sub('&', '', code)
        # code = re.findall('[0-9]+', code)[0]
        # code = re.findall('\d+', code)[0]
        # code = re.match('\d+', code)[0]

        # 영화포스터
        img = movie.find('img')
        img_url = img['src']

        # Image 폴더존재여부 확인
        if os.path.exists('./images') is False:
            os.mkdir('images')

        # 포스터 이미지 다운로드
        wget.download(img_url, f'./images/{code}.jpg')

        # 큰 포스터 이미지 다운로드
        origin_url = img_url.replace('174x246', '600x800')
        wget.download(origin_url, f'./images/{code}_origin.jpg')

        # 영화제목
        title = movie.find('div', class_='area_text_box')
        title = title.text.strip()

        info_list = movie.select('dl', class_='info_group')

        # 영화장르, 상영시간
        _, category, running_time = info_list[0].text.strip().split(' ')

        # 개봉일, 평점
        _, open_date, _, score = info_list[1].text.strip().split(' ')

        # 출연배우
        if len(info_list[2].text) != 0:
            actors = info_list[2].text
            actors = actors.replace('출연', '')
            actors = actors.strip()
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
        break
    except Exception as e:
        ic(e)

print('Crawling is done!!!')