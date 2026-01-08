#!/usr/bin/env python3
"""
Module xuất dữ liệu sang định dạng JSON tùy chỉnh
Export data to custom JSON format with pagination
"""

import json
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs


def extract_gp_id(google_play_link):
    """Trích xuất Google Play ID từ link"""
    if not google_play_link or google_play_link == "N/A":
        return ""
    
    try:
        parsed = urlparse(google_play_link)
        query_params = parse_qs(parsed.query)
        if 'id' in query_params:
            return query_params['id'][0]
    except:
        pass
    
    return ""


def wrap_in_paragraphs(text):
    """Wrap text trong <p> tags"""
    if not text or text == "N/A":
        return ""
    
    # Nếu đã có <p> tags thì return luôn
    if '<p>' in text:
        return text
    
    # Split theo newline và wrap mỗi đoạn
    paragraphs = text.split('\n')
    wrapped = []
    for p in paragraphs:
        p = p.strip()
        if p:
            wrapped.append(f"<p>{p}</p>")
    
    return '\n'.join(wrapped) if wrapped else f"<p>{text}</p>"


def parse_category(categories_path):
    """Parse category từ breadcrumb path"""
    if not categories_path or categories_path == "N/A":
        return {"name": "Games", "slug": "games"}, {"name": "Other", "slug": "other"}
    
    parts = [p.strip() for p in categories_path.split('>')]
    
    # Main category (Games/Apps)
    main_cat = parts[0] if len(parts) > 0 else "Games"
    main_slug = main_cat.lower()
    
    # Subcategory
    sub_cat = parts[1] if len(parts) > 1 else "Other"
    sub_slug = sub_cat.lower().replace(' ', '-')
    
    return (
        {"name": main_cat, "slug": main_slug},
        {"name": sub_cat, "slug": sub_slug}
    )


def convert_to_custom_format(article):
    """Convert một bài viết sang định dạng tùy chỉnh"""
    
    # Parse category
    category, subcategory = parse_category(article.get('categories', ''))
    
    # Parse images
    images_str = article.get('images', '')
    if images_str and images_str != "N/A":
        image_list = [img.strip() for img in images_str.split('|') if img.strip()]
    else:
        image_list = []
    
    # Thumbnail (ảnh đầu tiên)
    thumbnail = image_list[0] if image_list else ""
    
    # Poster (cũng là ảnh đầu tiên hoặc có thể khác)
    poster = thumbnail
    
    # Screenshots
    ss_images = [{"ss_url": img} for img in image_list]
    
    # MOD info
    mod_info = article.get('mod_info', '')
    if mod_info == "N/A":
        mod_info = ""
    
    # Prepare download links
    download_links = []
    if article.get('download_link') and article['download_link'] != "N/A":
        download_links.append({
            "download_name": "APK",
            "download_size": article.get('size', ''),
            "download_url": article.get('download_link', ''),
            "download_version": article.get('version', ''),
            "download_mod_info": mod_info
        })
    
    # Extract version from title if needed
    version = article.get('version', '')
    if version == "N/A" or not version:
        # Try to extract from title
        title = article.get('title', '')
        version_match = re.search(r'v?(\d+\.[\d.]+)', title)
        if version_match:
            version = version_match.group(1)
    
    # Build custom format
    custom_article = {
        "title": article.get('title', ''),
        "description": wrap_in_paragraphs(article.get('content', '')),
        "thumbnail": thumbnail,
        "category": category,
        "subcategory": subcategory,
        "apktemplates": {
            "wp_description_GP": wrap_in_paragraphs(article.get('description', '')),
            "wp_mod_info_GP": wrap_in_paragraphs(mod_info),
            "wp_whatnews_GP": "",  # Có thể để trống hoặc generate
            "wp_title_GP": article.get('app_name', ''),
            "wp_version_GP": version,
            "wp_developers_GP": article.get('publisher', ''),
            "wp_sizes_GP": article.get('size', ''),
            "wp_GP_ID": extract_gp_id(article.get('google_play_link', '')),
            "wp_mods": mod_info,
            "avg_rating": article.get('rating', ''),
            "total_votes": article.get('rating_count', ''),
            "repeatable_download_link": download_links,
            "ss_images": ss_images,
            "wp_poster_GP": poster
        }
    }
    
    return custom_article


def export_to_custom_format(articles_data, output_prefix="articles", 
                            posts_per_file=100, config=None):
    """
    Xuất dữ liệu sang định dạng JSON tùy chỉnh với phân trang
    
    Args:
        articles_data: List các bài viết
        output_prefix: Prefix cho tên file output
        posts_per_file: Số bài viết tối đa mỗi file
        config: Dict cấu hình cho info section
    """
    
    if not articles_data:
        print("⚠️  Không có dữ liệu để export!")
        return []
    
    # Default config
    default_config = {
        "theme_name": "liteapks",
        "theme_author": "admin",
        "theme_developer": "LITEAPKS Team",
        "theme_buy_link": "https://liteapks.com",
        "website": "https://liteapks.com",
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    if config:
        default_config.update(config)
    
    # Convert tất cả bài viết
    print(f"\n🔄 Đang convert {len(articles_data)} bài viết sang định dạng mới...")
    converted_posts = []
    
    for idx, article in enumerate(articles_data, 1):
        try:
            custom_article = convert_to_custom_format(article)
            converted_posts.append(custom_article)
            if idx % 10 == 0:
                print(f"  ✓ Đã convert {idx}/{len(articles_data)} bài viết...")
        except Exception as e:
            print(f"  ❌ Lỗi khi convert bài {idx}: {e}")
    
    print(f"✅ Convert thành công {len(converted_posts)} bài viết")
    
    # Split thành nhiều file nếu cần
    total_files = (len(converted_posts) + posts_per_file - 1) // posts_per_file
    output_files = []
    
    print(f"\n📦 Đang chia thành {total_files} file (tối đa {posts_per_file} bài/file)...")
    
    for file_idx in range(total_files):
        start_idx = file_idx * posts_per_file
        end_idx = min(start_idx + posts_per_file, len(converted_posts))
        
        posts_chunk = converted_posts[start_idx:end_idx]
        
        # Tạo output structure
        output_data = {
            "info": default_config.copy(),
            "posts": posts_chunk
        }
        
        # Thêm thông tin page vào info
        output_data["info"]["page"] = file_idx + 1
        output_data["info"]["total_pages"] = total_files
        output_data["info"]["posts_in_page"] = len(posts_chunk)
        output_data["info"]["total_posts"] = len(converted_posts)
        
        # Tên file
        if total_files == 1:
            filename = f"{output_prefix}.json"
        else:
            filename = f"{output_prefix}_{file_idx + 1}.json"
        
        # Lưu file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        
        output_files.append(filename)
        print(f"  ✅ File {file_idx + 1}/{total_files}: {filename} ({len(posts_chunk)} bài)")
    
    print(f"\n🎉 Hoàn thành! Đã tạo {len(output_files)} file JSON")
    return output_files


def main():
    """Hàm chính để test"""
    import sys
    
    # Đọc dữ liệu từ file JSON gốc
    input_file = "liteapks_articles.json"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {input_file}")
        print("💡 Hãy chạy sitemap_scraper.py trước!")
        sys.exit(1)
    
    print("="*70)
    print("📤 XUẤT DỮ LIỆU SANG ĐỊNH DẠNG TÙY CHỈNH")
    print("="*70)
    
    # Cấu hình
    config = {
        "theme_name": "liteapks",
        "theme_author": "admin",
        "theme_developer": "LITEAPKS Team",
        "theme_buy_link": "https://liteapks.com",
        "website": "https://liteapks.com",
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Export với cấu hình
    posts_per_file = 50  # Có thể thay đổi
    
    print(f"\n⚙️  Cấu hình:")
    print(f"  • Số bài viết mỗi file: {posts_per_file}")
    print(f"  • Website: {config['website']}")
    print(f"  • Theme: {config['theme_name']}")
    
    output_files = export_to_custom_format(
        articles,
        output_prefix="liteapks_custom",
        posts_per_file=posts_per_file,
        config=config
    )
    
    # Hiển thị thống kê
    print(f"\n📊 THỐNG KÊ:")
    print(f"  • Tổng số bài viết: {len(articles)}")
    print(f"  • Số file đã tạo: {len(output_files)}")
    print(f"  • Files: {', '.join(output_files)}")
    
    # Hiển thị mẫu
    if output_files:
        print(f"\n📄 XEM MẪU FILE ĐẦU TIÊN:")
        with open(output_files[0], 'r', encoding='utf-8') as f:
            sample = json.load(f)
        
        print(f"\n  Info:")
        for key, value in sample['info'].items():
            print(f"    • {key}: {value}")
        
        if sample['posts']:
            print(f"\n  Bài viết đầu tiên:")
            post = sample['posts'][0]
            print(f"    • Title: {post['title'][:60]}...")
            print(f"    • Category: {post['category']['name']} > {post['subcategory']['name']}")
            print(f"    • Version: {post['apktemplates']['wp_version_GP']}")
            print(f"    • Rating: {post['apktemplates']['avg_rating']}/5")
            print(f"    • Screenshots: {len(post['apktemplates']['ss_images'])} ảnh")


if __name__ == "__main__":
    main()
