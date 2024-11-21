import json
import re
import scrapy
from scrapy.crawler import CrawlerProcess

# Load danh sách URL từ file JSON
with open('data/all_urls.json', 'r') as file:
    all_urls = json.load(file)

class CustomSpider(scrapy.Spider):
    name = 'custom_spider'
    start_urls = all_urls[100:]  # Bắt đầu crawl từ URL thứ 100

    # Bộ đếm số lượng request
    request_count = 0

    def parse(self, response):
        self.request_count += 1
        description = ""

        # Lấy tiêu đề (thẻ h1)
        review_title = response.css('h1.product-title::text').get()
        h1_tag = review_title.strip() if review_title else ""

        # Lấy giá
        price = response.css('span.woocommerce-Price-amount').get().strip() if response.css('span.woocommerce-Price-amount') else ""

        # Lấy nội dung mô tả (thẻ div)
        ck_contents = response.css('div.woocommerce-Tabs-panel--description')
        for ck_content in ck_contents:
            for element in ck_content.xpath('./*'):
                if element.root.tag in ['h2', 'h3', 'p', 'ul']:
                    description += ' '.join(element.css('::text').getall()).strip() + "\n"

        # Lấy danh sách các URL hình ảnh
        image_urls = [element.css('img::attr(data-large_image)').get() for element in response.css('div.woocommerce-product-gallery__image')]

        # Xử lý dữ liệu và yield kết quả
        data = {
            "url": response.url,
            "content": re.sub(
                "Hoa Tươi My My luôn là lựa chọn tốt nhất...",
                "", description),
            "price": price,
            "title": h1_tag,
            "image_urls": image_urls
        }
        yield data

        self.logger.info(f"Số lượng request đã thực hiện: {self.request_count}")
        self.logger.info(f"Đã crawl: {response.url}")

# Hàm chạy Scrapy
def run_spider():
    process = CrawlerProcess({
        'LOG_LEVEL': 'INFO',
        'FEEDS': {
            'data/output.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
            },
        },
        'CLOSESPIDER_TIMEOUT': 600,  # Đóng spider sau 10 phút
        'DOWNLOAD_DELAY': 3,  # Thời gian nghỉ giữa các request
    })
    process.crawl(CustomSpider)
    process.start()

# Nếu chạy script này, thực hiện việc crawl
if __name__ == '__main__':
    run_spider()
