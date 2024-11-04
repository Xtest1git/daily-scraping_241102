import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_new_data():
    urls = [
        "https://movie.eroterest.net/site/s/18511/?word=&page=1",
        "https://movie.eroterest.net/site/s/18511/?word=&page=2",
        "https://movie.eroterest.net/site/s/18651"
    ]

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",  # 最新のUser-Agentに変更
    "Referer": "https://movie.eroterest.net"
}

    data = []

    for url in urls:
        response = requests.get(url, headers=headers)
        print(f"Fetching URL: {url}, Status Code: {response.status_code}")  # デバッグ用

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup.prettify())  # HTML内容を出力して確認

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

    return data
