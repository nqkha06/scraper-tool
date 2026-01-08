#!/usr/bin/env python3
"""
Script để so sánh và hiển thị sự khác biệt giữa phiên bản cũ và mới
"""

import json

def compare_versions():
    """So sánh dữ liệu thu thập được"""
    
    print("="*70)
    print("🔍 SO SÁNH PHIÊN BẢN CŨ VÀ MỚI")
    print("="*70)
    
    # Đọc dữ liệu mới
    with open('liteapks_articles.json', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    if not new_data:
        print("❌ Không có dữ liệu mới!")
        return
    
    sample = new_data[0]
    
    print("\n📊 THỐNG KÊ TRƯỜNG DỮ LIỆU:")
    print(f"  ✅ Phiên bản cũ: 12 trường")
    print(f"  ✅ Phiên bản mới: {len(sample)} trường")
    print(f"  📈 Tăng thêm: {len(sample) - 12} trường (+{((len(sample)-12)/12*100):.0f}%)")
    
    print("\n📋 CÁC TRƯỜNG DỮ LIỆU MỚI:")
    
    old_fields = [
        'url', 'title', 'app_name', 'publisher', 'genre', 
        'size', 'version', 'mod_info', 'download_link', 
        'content_preview', 'images', 'scraped_at'
    ]
    
    new_fields = list(sample.keys())
    added_fields = [f for f in new_fields if f not in old_fields and f != 'lastmod']
    
    print("\n✨ TRƯỜNG MỚI ĐƯỢC THÊM:")
    for i, field in enumerate(added_fields, 1):
        value = sample[field]
        val_str = str(value)
        if len(val_str) > 50:
            val_str = val_str[:50] + "..."
        print(f"  {i:2}. {field:20} = {val_str}")
    
    print("\n📝 SO SÁNH CHI TIẾT MỘT BÀI VIẾT:")
    print(f"\n🎮 {sample['title'][:60]}...")
    print("\n" + "-"*70)
    
    # Thông tin cơ bản (đã có từ trước)
    print("\n📌 THÔNG TIN CƠ BẢN (Đã có):")
    print(f"  • App Name: {sample['app_name']}")
    print(f"  • Publisher: {sample['publisher']}")
    print(f"  • Genre: {sample['genre']}")
    print(f"  • Size: {sample['size']}")
    print(f"  • Version: {sample['version']}")
    
    # Thông tin mới
    print("\n✨ THÔNG TIN MỚI (Vừa thêm):")
    print(f"  • Description: {sample['description'][:60]}...")
    print(f"  • Author: {sample['author']}")
    print(f"  • Categories: {sample['categories']}")
    print(f"  • OS: {sample['operating_system']}")
    print(f"  • Price: {sample['price']}")
    print(f"  • Rating: {sample['rating']}/5 ({sample['rating_count']} votes)")
    print(f"  • Published: {sample['published_time']}")
    print(f"  • Modified: {sample['modified_time']}")
    print(f"  • Google Play: {sample['google_play_link'][:50]}...")
    print(f"  • Images: {sample['image_count']} ảnh (tăng từ 5 → 10 max)")
    print(f"  • Content: {len(sample['content'])} ký tự (tăng từ 500 → 800)")
    
    # MOD Info so sánh
    print("\n🎯 MOD INFO - SO SÁNH:")
    print("  Cũ: Chỉ lấy từ bảng (1 dòng)")
    print(f"  Mới: Lấy chi tiết từ accordion")
    print(f"       → {sample['mod_info'][:60]}...")
    
    print("\n" + "="*70)
    print("✅ CODE MỚI ĐÃ TỐI ƯU VÀ LẤY ĐẦY ĐỦ THÔNG TIN HƠN!")
    print("="*70)
    
    # Tổng kết
    print("\n📊 TỔNG KẾT CẢI TIẾN:")
    improvements = [
        "Thêm 12+ trường dữ liệu mới",
        "Lấy metadata từ JSON-LD Schema",
        "Rating & số lượng đánh giá chi tiết",
        "Thông tin tác giả & thời gian xuất bản",
        "Breadcrumb/categories đầy đủ",
        "MOD info chi tiết từ accordion",
        "Google Play link chính thức",
        "Nội dung mô tả dài hơn 60%",
        "Số lượng ảnh tăng gấp đôi",
        "Thêm thông tin OS, Price"
    ]
    
    for i, imp in enumerate(improvements, 1):
        print(f"  {i:2}. ✅ {imp}")
    
    print("\n💡 ĐỂ SCRAPE TOÀN BỘ WEBSITE:")
    print("  1. Mở file sitemap_scraper.py")
    print("  2. Đổi max_articles=5 thành max_articles=None")
    print("  3. Chạy lại: python sitemap_scraper.py")
    print(f"  4. Sẽ scrape {len(new_data)} → ~16,692 bài viết")


if __name__ == "__main__":
    compare_versions()
