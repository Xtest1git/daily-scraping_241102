import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import time

# スクレイピング対象のURL
urls = [
    "https://movie.eroterest.net/site/s/18511/?word=&page=1",
    "https://movie.eroterest.net/site/s/18511/?word=&page=2",
    "https://movie.eroterest.net/site/s/18651"
]

# ヘッダーを設定して、リクエストがブロックされないようにする
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Referer": "https://movie.eroterest.net",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

# データを保存するリスト
data = []

# 各URLからデータをスクレイピング
for url in urls:
    response = requests.get(url, headers=headers)
    print(f"Fetching URL: {url}, Status Code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='itemWrapper')
        if not items:
            print(f"No items found on {url}")
        for item in items:
            title = item.find('div', class_='itemTitle').get_text().strip()
            link = item.find('a')['href']
            img_url = item.find('img')['src']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url

            # 現在の日時を取得してフォーマット
            scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append([title, link, img_url, scrape_time])
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")
    
    # 各リクエストの間に待機
    time.sleep(2)  # 2秒待機

# データをCSVファイルに書き込む
csv_file_path = "data.csv"
existing_titles = set()
if os.path.exists(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        for row in reader:
            if row:
                existing_titles.add(row[0])

with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if os.stat(csv_file_path).st_size == 0:
        writer.writerow(['title', 'link', 'image_url', 'scrape_time'])
    for item in data:
        if item[0] not in existing_titles:
            writer.writerow(item)

print("Scraping and data saving completed successfully.")
