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
            print(f"No items found on {url}. The structure might have changed.")
        
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
                data.append([title, link, img_url, scrape_time])
            except AttributeError as e:
                print(f"Error parsing item on {url}: {e}")
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

# デバッグ用の出力
print(f"Total items scraped: {len(data)}")

# データをCSVファイルに書き込む
csv_file_path = "data.csv"

# ファイルが存在する場合は、既存のデータを取得
existing_titles = set()
if os.path.exists(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # ヘッダーをスキップ
        for row in reader:
            if row:
                existing_titles.add(row[0])  # タイトルをセットに追加

# 新しいデータをCSVファイルに書き込む
with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if os.stat(csv_file_path).st_size == 0:  # ファイルが空の場合、ヘッダーを書き込む
        writer.writerow(['title', 'link', 'image_url', 'scrape_time'])
    for item in data:
        if item[0] not in existing_titles:  # 既存のデータと重複しない場合に書き込む
            writer.writerow(item)

print("Scraping and data saving completed successfully.")
