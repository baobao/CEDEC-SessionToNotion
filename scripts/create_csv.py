# CEDEC2020のセッションリストをNotionにインポートするためのCSVを作成するスクリプト
# セッション名,date,資料公開,発表者,url
import requests
import re
from bs4 import BeautifulSoup

output = 'cedec2020_session2.csv'
load_url = "https://cedec.cesa.or.jp/2020/session"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

result_csv = 'title,date,資料公開,author,url\n'

sessions = soup.find_all(class_ = 'pl-0')
for session in sessions:
    link = session.find(class_ = "col-12 mt-1")
    detail_url = link.find('a').get('href')

    # detail
    detail_html = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_html.content, 'html.parser')
    info_list = detail_soup.find_all(class_ = "detail-session-skill ml-0 ml-sm-4")

    # 09月02日(水)09:25〜10:45 => Sep 2 2020 09:25-10:45
    date = info_list[1].text.replace(' ', '').replace('\n', '')
    is_open_slide = info_list[2].text.replace(' ', '').replace('\n', '')


    pattern = r'^[0-9]*月0([0-9])日\(.\)([0-9]*):([0-9]*)〜([0-9]*):([0-9]*)'
    match = re.match(pattern, date)
    if match:        
        day = match.group(1)
        start_h = match.group(2)
        start_m = match.group(3)
        end_h = match.group(4)
        end_m = match.group(5)
        import_date = "Sep {} 2020 {}:{}-{}:{}".format(day, start_h,start_m, end_h, end_m)
    
    if is_open_slide == '予定あり':
        is_open_slide = 'あり'
    else:
        is_open_slide = 'なし'

    title = session.find(class_ = 'session-title')
    author = session.find(class_ = 'medium-text gray-light')
    # インポートに失敗するので「"」を削除
    title = title.text.replace(' ', '').replace(',', '').replace('"', '')
    author = author.text.replace(' ', '').replace('\n', '').replace(',', '')
    
    result_csv += "{},{},{},{},{}\n".format(title, import_date, is_open_slide, author, detail_url)

file_path = output
fileobj = open(file_path, 'w', encoding = 'utf_8')
fileobj.write(result_csv)
fileobj.close()
