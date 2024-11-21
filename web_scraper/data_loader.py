import requests
import xml.etree.ElementTree as ET
import json

# URLs của sitemap
sitemap_urls = [
    'https://hoatuoimymy.com/product-sitemap1.xml',
    'https://hoatuoimymy.com/product-sitemap2.xml'
]

all_urls = []

# Hàm tải và phân tích XML từ sitemap
def fetch_sitemap(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra trạng thái request
        root = ET.fromstring(response.content)
        # Lấy tất cả các thẻ <loc> chứa URL
        for url_element in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            all_urls.append(url_element.text)
    except Exception as e:
        print(f"Lỗi khi tải hoặc phân tích {url}: {e}")

# Tải và phân tích các sitemap
def load_sitemap():
    for sitemap_url in sitemap_urls:
        fetch_sitemap(sitemap_url)

    # Ghi các URL vào file JSON
    with open('data/all_urls.json', 'w') as f:
        json.dump(all_urls, f, indent=4)

    print(f"Đã tải {len(all_urls)} URL và lưu vào data/all_urls.json")

# Nếu chạy script này, thực hiện việc tải sitemap
if __name__ == '__main__':
    load_sitemap()
