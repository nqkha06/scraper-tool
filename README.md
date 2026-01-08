# Công cụ Thu thập Dữ liệu Yoast Sitemap

Tool Python để thu thập dữ liệu từ các bài viết trong Yoast sitemap của liteapks.com

## Tính năng

- ✅ Tự động phát hiện và đọc tất cả sitemap con
- ✅ Thu thập thông tin chi tiết từ mỗi bài viết:
  - Tiêu đề
  - Tên ứng dụng
  - Nhà phát hành
  - Thể loại
  - Kích thước
  - Phiên bản
  - Thông tin MOD
  - Link download
  - Nội dung preview
  - Hình ảnh
- ✅ Lưu dữ liệu vào CSV và JSON
- ✅ Có delay để tránh bị chặn

## Cài đặt & Sử dụng

### Cách 1: Sử dụng script tự động (Khuyến nghị)

```bash
./run.sh
```

Script này sẽ tự động:
- Tạo virtual environment nếu chưa có
- Cài đặt dependencies
- Chạy scraper

### Cách 2: Chạy thủ công

```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt virtual environment
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy scraper
python sitemap_scraper.py

# Xem phân tích dữ liệu
python view_data.py
```

## Cấu hình

Mở file `sitemap_scraper.py` và chỉnh sửa:

```python
# Giới hạn số bài viết (None = scrape tất cả)
scraper.scrape_all(max_articles=50, delay=1)

# Để scrape TẤT CẢ bài viết:
scraper.scrape_all(max_articles=None, delay=1)
```

### Tham số:
- `max_articles`: Số lượng bài viết tối đa (None = không giới hạn)
- `delay`: Thời gian chờ giữa các request (giây)

## Kết quả

Tool sẽ tạo ra 2 file:
- `liteapks_articles.csv` - Dữ liệu dạng bảng
- `liteapks_articles.json` - Dữ liệu dạng JSON

### Xem phân tích dữ liệu

Sau khi scrape xong, bạn có thể xem thống kê:

```bash
python view_data.py
```

Sẽ hiển thị:
- Tổng số bài viết
- Thể loại phổ biến
- Nhà phát hành
- Số bài có MOD info
- Số bài có link download
- 5 bài viết mẫu

## Cấu trúc dữ liệu

Mỗi bài viết chứa **25+ trường dữ liệu**:

```json
{
  "url": "https://liteapks.com/...",
  "title": "Tiêu đề đầy đủ",
  "description": "Mô tả ngắn (meta)",
  "app_name": "Tên ứng dụng",
  "publisher": "Nhà phát hành",
  "author": "Tác giả bài viết",
  "genre": "Thể loại",
  "categories": "Games > Sports",
  "size": "125 MB",
  "version": "2.1.1",
  "operating_system": "Android",
  "price": "Free",
  "mod_info": "Free Kits Receive; No ADS",
  "rating": "4.5",
  "rating_count": "13",
  "google_play_link": "https://play.google.com/...",
  "download_link": "https://liteapks.com/download/...",
  "published_time": "2022-06-28T09:53:48+00:00",
  "modified_time": "2022-06-28T09:54:00+00:00",
  "content": "Nội dung mô tả chi tiết (800 ký tự)...",
  "images": "url1|url2|url3...",
  "image_count": 5,
  "scraped_at": "2026-01-08T..."
}
```

**Nâng cấp so với phiên bản cũ:**
- ✅ Thêm 15+ trường dữ liệu mới
- ✅ Lấy metadata từ JSON-LD schema
- ✅ Rating & số lượng đánh giá
- ✅ Thông tin tác giả, thời gian xuất bản
- ✅ Breadcrumb/categories đầy đủ
- ✅ MOD info chi tiết từ accordion
- ✅ Google Play link chính thức
- ✅ Nội dung mô tả dài hơn (800 ký tự)
- ✅ Nhiều hình ảnh hơn (tối đa 10)
  "genre": "Thể loại",
  "size": "Dung lượng",
  "version": "Phiên bản",
  "mod_info": "Thông tin MOD",
  "download_link": "Link download",
  "content_preview": "Nội dung...",
  "images": "URL1, URL2, ...",
  "lastmod": "Ngày cập nhật",
  "scraped_at": "Thời gian scrape"
}
```

## Lưu ý

- Tool có delay 1 giây giữa các request để tránh bị chặn
- Nên chạy test với số lượng nhỏ trước (max_articles=50)
- Có thể mất nhiều thời gian nếu scrape toàn bộ sitemap

## Ví dụ sử dụng nâng cao

```python
from sitemap_scraper import YoastSitemapScraper

# Khởi tạo
scraper = YoastSitemapScraper("https://liteapks.com")

# Scrape 100 bài viết đầu tiên
scraper.scrape_all(max_articles=100, delay=2)

# Lưu kết quả
scraper.save_to_csv('my_data.csv')
scraper.save_to_json('my_data.json')

# Xem dữ liệu
print(f"Đã thu thập: {len(scraper.articles_data)} bài viết")
```

## Yêu cầu

- Python 3.7+
- requests
- beautifulsoup4
- lxml
