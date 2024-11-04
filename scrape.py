import requests
from bs4 import BeautifulSoup
from datetime import datetime

# スクレイピング対象のURL
urls = [
    "https://movie.eroterest.net/site/s/18511/?word=&page=1",
    "https://movie.eroterest.net/site/s/18511/?word=&page=2",
    "https://movie.eroterest.net/site/s/18651"
]

# ヘッダーを設定して、リクエストがブロックされないようにする
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# get_new_data関数を定義してスクレイピングデータを返す
def get_new_data():
    data = []
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
                data.append({
                    "title": title,
                    "link": link,
                    "image_url": img_url,
                    "scrape_time": scrape_time
                })
        else:
            print(f"Failed to retrieve {url}, status code: {response.status_code}")

    return data
