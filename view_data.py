#!/usr/bin/env python3
"""
Script xem và phân tích dữ liệu đã thu thập
"""

import json
import csv
from collections import Counter

def analyze_data():
    """Phân tích dữ liệu đã thu thập"""
    
    # Đọc file JSON
    try:
        with open('liteapks_articles.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Không tìm thấy file liteapks_articles.json")
        print("Vui lòng chạy sitemap_scraper.py trước!")
        return
    
    print("="*60)
    print("   PHÂN TÍCH DỮ LIỆU ĐÃ THU THẬP")
    print("="*60 + "\n")
    
    print(f"📊 Tổng số bài viết: {len(data)}\n")
    
    # Thống kê theo thể loại
    genres = [item['genre'] for item in data if item['genre'] != 'N/A']
    if genres:
        print("📁 Thể loại phổ biến:")
        genre_counts = Counter(genres).most_common(10)
        for genre, count in genre_counts:
            print(f"  • {genre}: {count} bài")
    
    # Thống kê theo nhà phát hành
    print("\n🏢 Nhà phát hành:")
    publishers = [item['publisher'] for item in data if item['publisher'] != 'N/A']
    if publishers:
        publisher_counts = Counter(publishers).most_common(5)
        for pub, count in publisher_counts:
            print(f"  • {pub}: {count} ứng dụng")
    
    # Thống kê có MOD info
    print("\n🔧 Thông tin MOD:")
    with_mod = sum(1 for item in data if item['mod_info'] != 'N/A')
    print(f"  • Có thông tin MOD: {with_mod}/{len(data)} bài")
    
    # Thống kê có link download
    print("\n📥 Link download:")
    with_download = sum(1 for item in data if item['download_link'] != 'N/A')
    print(f"  • Có link download: {with_download}/{len(data)} bài")
    
    # Hiển thị một số bài viết mẫu
    print("\n📄 Mẫu dữ liệu (5 bài đầu tiên):")
    print("-" * 60)
    for idx, item in enumerate(data[:5], 1):
        print(f"\n{idx}. {item['title']}")
        print(f"   URL: {item['url']}")
        print(f"   Thể loại: {item['genre']}")
        print(f"   Phiên bản: {item['version']}")
        if item['mod_info'] != 'N/A':
            print(f"   MOD: {item['mod_info'][:50]}...")
    
    print("\n" + "="*60)
    print(f"✅ Dữ liệu đã được lưu vào:")
    print(f"   • liteapks_articles.csv")
    print(f"   • liteapks_articles.json")
    print("="*60)

if __name__ == "__main__":
    analyze_data()
