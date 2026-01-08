# 📤 HƯỚNG DẪN XUẤT ĐỊNH DẠNG TÙY CHỈNH

## 🎯 Tổng quan

Tool hỗ trợ xuất dữ liệu sang **định dạng JSON tùy chỉnh** phù hợp với các theme WordPress hoặc hệ thống khác.

---

## 📋 Định dạng Output

```json
{
    "info": {
        "theme_name": "liteapks",
        "theme_author": "admin",
        "theme_developer": "LITEAPKS Team",
        "theme_buy_link": "https://liteapks.com",
        "website": "https://liteapks.com",
        "created": "2026-01-08",
        "page": 1,
        "total_pages": 1,
        "posts_in_page": 50,
        "total_posts": 50
    },
    "posts": [
        {
            "title": "App Name MOD APK v1.0.0 (MOD Features)",
            "description": "<p>Mô tả đầy đủ...</p>",
            "thumbnail": "https://...",
            "category": {
                "name": "Games",
                "slug": "games"
            },
            "subcategory": {
                "name": "Action",
                "slug": "action"
            },
            "apktemplates": {
                "wp_description_GP": "<p>Mô tả ngắn</p>",
                "wp_mod_info_GP": "<p>MOD info</p>",
                "wp_whatnews_GP": "<p>What's new</p>",
                "wp_title_GP": "App Name",
                "wp_version_GP": "1.0.0",
                "wp_developers_GP": "Developer Name",
                "wp_sizes_GP": "125 MB",
                "wp_GP_ID": "com.package.name",
                "wp_mods": "MOD Features",
                "avg_rating": "4.5",
                "total_votes": "1000",
                "repeatable_download_link": [
                    {
                        "download_name": "APK",
                        "download_size": "125 MB",
                        "download_url": "https://...",
                        "download_version": "1.0.0",
                        "download_mod_info": "MOD info"
                    }
                ],
                "ss_images": [
                    {"ss_url": "https://..."},
                    {"ss_url": "https://..."}
                ],
                "wp_poster_GP": "https://..."
            }
        }
    ]
}
```

---

## 🚀 Cách sử dụng

### 1. Scrape dữ liệu trước

```bash
# Chạy scraper
python sitemap_scraper.py
```

### 2. Export sang định dạng tùy chỉnh

**Cách 1: Tự động (khi chạy scraper)**
```bash
# Scraper sẽ tự động export sau khi hoàn thành
python sitemap_scraper.py
```

**Cách 2: Export riêng**
```bash
# Export từ file JSON đã có
python export_custom_format.py
```

---

## ⚙️ Cấu hình

### Thay đổi số bài viết mỗi file

Mở file `export_custom_format.py` và sửa:

```python
posts_per_file = 50  # Thay đổi số này

# Ví dụ:
posts_per_file = 100  # 100 bài/file
posts_per_file = 25   # 25 bài/file
```

### Tùy chỉnh thông tin Info

Trong `sitemap_scraper.py`, sửa phần config:

```python
config = {
    "theme_name": "modyolo",          # Tên theme
    "theme_author": "admin",          # Tác giả
    "theme_developer": "Your Name",   # Developer
    "theme_buy_link": "https://...",  # Link mua theme
    "website": "https://yoursite.com" # Website
}
```

---

## 📦 Phân trang tự động

Nếu có **nhiều bài viết**, tool sẽ tự động chia thành nhiều file:

```
Ví dụ: 150 bài viết, cấu hình 50 bài/file

Output:
- liteapks_custom_1.json (50 bài)
- liteapks_custom_2.json (50 bài)
- liteapks_custom_3.json (50 bài)
```

Mỗi file sẽ có thông tin page:
```json
{
    "info": {
        "page": 1,
        "total_pages": 3,
        "posts_in_page": 50,
        "total_posts": 150
    }
}
```

---

## 🔄 Mapping dữ liệu

| Dữ liệu gốc | Định dạng mới | Ghi chú |
|-------------|---------------|---------|
| title | title | Giữ nguyên |
| content | description | Wrap trong `<p>` tags |
| images[0] | thumbnail | Ảnh đầu tiên |
| categories | category.name | Parse từ breadcrumb |
| genre | subcategory.name | Subcategory |
| description | wp_description_GP | Meta description |
| mod_info | wp_mod_info_GP | Wrap trong `<p>` |
| app_name | wp_title_GP | Tên app |
| version | wp_version_GP | Version |
| publisher | wp_developers_GP | Developer |
| size | wp_sizes_GP | Kích thước |
| google_play_link | wp_GP_ID | Trích xuất package ID |
| mod_info | wp_mods | Plain text |
| rating | avg_rating | Điểm đánh giá |
| rating_count | total_votes | Số lượng votes |
| download_link | repeatable_download_link | Array of download links |
| images | ss_images | Array of screenshots |
| images[0] | wp_poster_GP | Banner image |

---

## 💡 Ví dụ sử dụng

### Scrape 100 bài và export (50 bài/file)

```python
# sitemap_scraper.py
scraper.scrape_all(max_articles=100, delay=1)

# Sẽ tạo:
# - liteapks_articles.csv
# - liteapks_articles.json
# - liteapks_custom_1.json (50 bài)
# - liteapks_custom_2.json (50 bài)
```

### Export lại với cấu hình khác

```python
# export_custom_format.py
from export_custom_format import export_to_custom_format
import json

# Đọc dữ liệu
with open('liteapks_articles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Export với cấu hình mới
config = {
    "theme_name": "custom_theme",
    "website": "https://mysite.com"
}

export_to_custom_format(
    data,
    output_prefix="custom_export",
    posts_per_file=25,  # 25 bài/file
    config=config
)
```

---

## 🎨 Features

✅ **Tự động chia file** khi vượt quá số bài cấu hình
✅ **HTML formatting** tự động wrap trong `<p>` tags
✅ **Google Play ID** tự động trích xuất từ link
✅ **Category parsing** từ breadcrumb path
✅ **Screenshots array** từ danh sách images
✅ **Download links array** với đầy đủ thông tin
✅ **Page info** với total_pages, posts_in_page
✅ **UTF-8 encoding** hỗ trợ tiếng Việt
✅ **Error handling** xử lý lỗi an toàn

---

## 📊 Kiểm tra output

```bash
# Xem thống kê
python -c "
import json
with open('liteapks_custom.json', 'r') as f:
    data = json.load(f)
print(f'Info: {data[\"info\"]}')
print(f'Posts: {len(data[\"posts\"])} bài')
"

# Xem bài đầu tiên
python -c "
import json
with open('liteapks_custom.json', 'r') as f:
    data = json.load(f)
post = data['posts'][0]
print(json.dumps(post, indent=2, ensure_ascii=False)[:500])
"
```

---

## 🔧 Troubleshooting

### Lỗi: Module not found

```bash
# Đảm bảo file export_custom_format.py cùng thư mục
ls -la export_custom_format.py

# Activate virtual environment
source venv/bin/activate
```

### Lỗi: File not found

```bash
# Chạy scraper trước
python sitemap_scraper.py

# Sau đó mới export
python export_custom_format.py
```

### Muốn thay đổi output folder

```python
# Trong export_custom_format.py
import os

output_dir = "custom_output"
os.makedirs(output_dir, exist_ok=True)

filename = os.path.join(output_dir, f"{output_prefix}.json")
```

---

## 📚 Tài liệu tham khảo

- [README.md](README.md) - Hướng dẫn tổng quan
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [CHANGELOG.md](CHANGELOG.md) - Lịch sử cập nhật
- [articles-demo.json](articles-demo.json) - File mẫu định dạng

---

**🎉 Chúc bạn sử dụng thành công!**
