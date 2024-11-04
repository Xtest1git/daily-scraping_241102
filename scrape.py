import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

urls = [
    "https://movie.eroterest.net/site/s/18511/?word=&page=1",
    "https://movie.eroterest.net/site/s/18511/?word=&page=2",
    "https://movie.eroterest.net/site/s/18651"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

data = []

for url in urls:
    print(f"Fetching URL: {url}")
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
            data.append([title, link, img_url, scrape_time])
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")

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
