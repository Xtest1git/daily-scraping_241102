import csv
from datetime import datetime, timedelta
from scrape import get_new_data  # scrape.py から get_new_data をインポート

# CSVファイルのパス
csv_file = 'data.csv'

# 有効期限（例: 30日）
valid_duration = timedelta(days=30)
today = datetime.today()

# 既存データを読み込む関数
def load_existing_data():
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = [row for row in reader]
            existing_titles = [row['title'] for row in existing_data]
        return existing_data, existing_titles
    except FileNotFoundError:
        return [], []

# 新しいデータをCSVに追加する関数
def append_to_csv(new_data):
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'link', 'image_url', 'scrape_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()  # ファイルが空の場合、ヘッダーを書き込む
        writer.writerows(new_data)

# メインの処理
def manage_data():
    existing_data, existing_titles = load_existing_data()
    new_data = get_new_data()
    unique_new_data = [item for item in new_data if item['title'] not in existing_titles]

    if unique_new_data:
        append_to_csv(unique_new_data)
        print(f"{len(unique_new_data)} new rows added.")
    else:
        print("No new data to add.")

    # 古いデータを削除
    filtered_data = [
        row for row in existing_data
        if today - datetime.strptime(row['scrape_time'], '%Y-%m-%d %H:%M:%S') <= valid_duration
    ]
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'link', 'image_url', 'scrape_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)
    print(f"{len(existing_data) - len(filtered_data)} old rows deleted.")

if __name__ == "__main__":
    manage_data()
