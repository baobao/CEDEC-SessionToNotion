# CEDEC2021のセッションリストをNotionにインポートするためのCSVを作成するスクリプト
# セッション名,date,資料公開,発表者,url
import requests
import re
from bs4 import BeautifulSoup
import os

output_dir = 'output'
os.mkdir(output_dir)

output = "{}/cedec2021_session.csv".format(output_dir)
load_url = "https://cedec.cesa.or.jp/2021/session"
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
    info_list = detail_soup.find_all(class_ = "detail-session-skill ml-0 ml-md-4")

    # 09月02日(水)09:25〜10:45 => Sep 2 2020 09:25-10:45
    date = info_list[1].text.replace(' ', '').replace('\n', '')
    is_open_slide = info_list[2].text.replace(' ', '').replace('\n', '')

    # 08月24日(火) 11:20〜 11:45
    pattern = r'.*[0-9]*月([0-9]*)日\(.\).*([0-9][0-9]):([0-9][0-9]).*〜.*([0-9][0-9]):([0-9][0-9])'
    match = re.match(pattern, date)
    import_date = ''
    if match:        
        day = match.group(1)
        start_h = match.group(2)
        start_m = match.group(3)
        end_h = match.group(4)
        end_m = match.group(5)
        # Augは8月開催なので判定なしで固定入力
        import_date = "Aug {} 2021 {}:{}-{}:{}".format(day, start_h,start_m, end_h, end_m)
    
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
