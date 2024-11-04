import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# スクレイピング対象のURL
urls = [
    "https://movie.eroterest.net/site/s/18511/?word=&page=1",
    "https://movie.eroterest.net/site/s/18511/?word=&page=2",
    "https://movie.eroterest.net/site/s/18651"
]

# ヘッダーを設定して、リクエストがブロックされないようにする
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://movie.eroterest.net"
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
            try:
                title = item.find('div', class_='itemTitle').get_text().strip()
                link = item.find('a')['href']
                img_url = item.find('img')['src']
                if img_url.startswith('//'):
                    img_url = 'https:' + img_url

                # 現在の日時を取得してフォーマット
                scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # データをリストに追加
                data.append({
                    "title": title,
                    "link": link,
                    "image_url": img_url,
                    "scrape_time": scrape_time
                })
            except AttributeError as e:
                print(f"Error parsing item on {url}: {e}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

# get_new_data 関数を定義して、データを返す
def get_new_data():
    return data

print("Scraping and data saving completed successfully.")
