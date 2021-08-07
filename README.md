# CEDEC SessionToNotion

CEDEC2021のセッションリストをカスタマイズしてNotionにインポートするためのCSVを作成するスクリプト

[NotionにまとめたCEDEC2021セッションリスト](https://www.notion.so/936b054353b14cbfb748f83b4f385327?v=1f841c200fc1467ea10e6dc5be57098b)


![image](https://user-images.githubusercontent.com/144386/128589043-508c693a-f577-4df8-960d-c10041355890.png)    
セッション名、日付、資料公開、発表者名、URLを一覧化したNotion

## Required

- BeautifulSoup
- requrests
- Python3


モジュールがインストールされていない人は下記のコマンドでインストール。

```shell
$ python3 -m pip install beautifulsoup4
$ python3 -m pip install requrests
```

## Usage

```shell
python3 scripts/create_csv.py
```

## 解説記事

[PythonとNotionを使ってCEDEC2020のセッションリストを見やすく一覧化してみる](https://note.com/ohbashunsuke/n/n97ef497a270c)