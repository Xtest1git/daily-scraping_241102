import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_new_data():
    # スクレイピング対象のURL
    urls = [
        "https://movie.eroterest.net/site/s/18511/?word=&page=1",
        "https://movie.eroterest.net/site/s/18511/?word=&page=2",
        "https://movie.eroterest.net/site/s/18651"
    ]

    # より新しい User-Agent を設定し、リクエストがブロックされないようにする
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "https://movie.eroterest.net",
        "Accept-Language": "en-US,en;q=0.9"
    }

    data = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            time.sleep(1)  # 各リクエストの間に1秒の遅延を追加
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
                    data.append({
                        'title': title,
                        'link': link,
                        'image_url': img_url,
                        'scrape_time': scrape_time
                    })
            else:
                print(f"Failed to retrieve {url}, status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while fetching {url}: {e}")

    return data
