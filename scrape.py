import requests
from bs4 import BeautifulSoup

# スクレイピングするURL
url = "https://example.com/scraping-page"

# HTTPリクエストを送信してページの内容を取得
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 新しいデータを保存するリスト
new_data = []

# データを抽出する（例: 画像URL、タイトル、リンク）
for item in soup.select(".item-class"):  # 適切なセレクタに変更してください
    image_url = item.select_one(".image-class")["src"]
    title = item.select_one(".title-class").text.strip()
    link = item.select_one(".link-class")["href"]

    # 新しいデータを辞書として追加
    new_data.append({
        "image_url": image_url,
        "title": title,
        "link": link
    })

# 新しいデータをreturnする
def get_new_data():
    return new_data
