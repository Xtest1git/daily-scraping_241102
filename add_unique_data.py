import csv
from datetime import datetime, timedelta
from scrape import get_new_data

# CSVファイルのパス
csv_file = 'data.csv'

# 有効期限（例: 30日）
valid_duration = timedelta(days=30)
today = datetime.today()

def load_existing_data():
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = [row for row in reader]
            existing_titles = [row['title'] for row in existing_data]
        return existing_data, existing_titles
    except FileNotFoundError:
        return [], []

def append_to_csv(new_data):
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'link', 'image_url', 'scrape_time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(new_data)

def manage_data():
    existing_data, existing_titles = load_existing_data()
    new_data = get_new_data()
    unique_new_data = [item for item in new_data if item['title'] not in existing_titles]

    if unique_new_data:
        append_to_csv(unique_new_data)
        print(f"{len(unique_new_data)} new rows added.")
    else:
        print("No new data to add.")

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
