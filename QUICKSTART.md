# Hướng dẫn Sử dụng Nhanh

## 🚀 Bắt đầu nhanh

```bash
# Bước 1: Chạy scraper
./run.sh

# Bước 2: Xem kết quả
source venv/bin/activate
python view_data.py
```

## 📂 Cấu trúc Project

```
bug/
├── sitemap_scraper.py    # Script chính thu thập dữ liệu
├── view_data.py          # Script phân tích & xem dữ liệu
├── run.sh                # Script chạy tự động
├── requirements.txt      # Danh sách dependencies
├── README.md             # Hướng dẫn chi tiết
├── QUICKSTART.md         # File này
├── venv/                 # Virtual environment (tự động tạo)
├── liteapks_articles.csv # Dữ liệu kết quả (CSV)
└── liteapks_articles.json # Dữ liệu kết quả (JSON)
```

## ⚙️ Tùy chỉnh

### Thay đổi số lượng bài viết

Mở file `sitemap_scraper.py` và tìm dòng:

```python
scraper.scrape_all(max_articles=50, delay=1)
```

Thay đổi:
- `max_articles=50` → `max_articles=100` (scrape 100 bài)
- `max_articles=None` (scrape TẤT CẢ)
- `delay=1` → `delay=2` (tăng thời gian chờ lên 2 giây)

### Scrape từ URL cụ thể

```python
# Trong file sitemap_scraper.py, thêm tham số sitemap_urls:
scraper.scrape_all(
    max_articles=100,
    delay=1,
    sitemap_urls=[
        "https://liteapks.com/post-sitemap.xml",
        "https://liteapks.com/post-sitemap2.xml"
    ]
)
```

## 📊 Dữ liệu thu thập

### Phiên bản mới: 24 trường dữ liệu (+100% so với cũ)

**Thông tin cơ bản:**
- url, title, description, app_name, publisher, author
- genre, categories, size, version, operating_system, price

**Đánh giá & Links:**
- rating, rating_count, mod_info
- google_play_link, download_link

**Thời gian & Nội dung:**
- published_time, modified_time, scraped_at
- content (800 ký tự), images (tối đa 10), image_count

### Ví dụ:
```
Title: Soccer Manager 2021 MOD APK v2.1.1
Rating: 4.5/5 (13 votes)
MOD: Disabled advertising display; Free kits
Categories: Games > Sports
Images: 5 ảnh
```

### So với phiên bản cũ:
- ✅ Tăng từ 12 → 24 trường (+100%)
- ✅ Thêm rating, author, categories, google_play_link
- ✅ Content tăng 500 → 800 ký tự (+60%)
- ✅ Images tăng tối đa 5 → 10 ảnh (+100%)
- **images**: Danh sách URL hình ảnh
- **lastmod**: Ngày cập nhật cuối
- **scraped_at**: Thời gian scrape

## 🛠️ Xử lý lỗi

### Lỗi timeout
Nếu gặp lỗi timeout, tăng giá trị `delay`:
```python
scraper.scrape_all(max_articles=50, delay=3)  # Tăng lên 3 giây
```

### Lỗi không tìm thấy sitemap
Tool sẽ tự động sử dụng danh sách sitemap backup.

### Lỗi cài đặt
```bash
# Xóa venv và cài lại
rm -rf venv
./run.sh
```

## 💡 Tips

1. **Test trước**: Luôn chạy với `max_articles=10` để test trước
2. **Backup**: Đổi tên file kết quả cũ trước khi scrape lại
3. **Tôn trọng server**: Không đặt `delay` quá nhỏ (< 1 giây)
4. **Lưu tiến độ**: Tool có thể bị gián đoạn, hãy backup dữ liệu thường xuyên

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra kết nối internet
2. Đảm bảo Python 3.7+ đã được cài đặt
3. Kiểm tra log output để xem lỗi cụ thể
4. Thử giảm `max_articles` và tăng `delay`

## 🎯 Ví dụ sử dụng

### Scrape 10 bài để test
```python
scraper.scrape_all(max_articles=10, delay=1)
```

### Scrape nhiều với delay cao
```python
scraper.scrape_all(max_articles=500, delay=2)
```

### Scrape tất cả (cẩn thận!)
```python
scraper.scrape_all(max_articles=None, delay=2)
# Lưu ý: Có thể mất vài giờ với hàng nghìn bài viết
```
