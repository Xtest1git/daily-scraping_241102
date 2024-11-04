import requests
from bs4 import BeautifulSoup
from datetime import datetime

# スクレイピング対象のURLリスト
urls = [
    "https://movie.eroterest.net/site/s/18511/?word=&page=1",
    "https://movie.eroterest.net/site/s/18511/?word=&page=2",
    "https://movie.eroterest.net/site/s/18651"
]

# HTTPリクエストヘッダー
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://movie.eroterest.net"
}

# 新しいデータを保存するリスト
new_data = []

# 各URLを処理
for url in urls:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='itemWrapper')

        for item in items:
            title = item.find('div', class_='itemTitle').get_text().strip()
            link = item.find('a')['href']
            img_url = item.find('img')['src']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url

            scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_data.append({
                'title': title,
                'link': link,
                'image_url': img_url,
                'scrape_time': scrape_time
            })
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

# 新しいデータを返す関数
def get_new_data():
    return new_data
