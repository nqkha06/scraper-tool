#!/bin/bash

# Script chạy công cụ scraper

echo "🚀 Khởi động Yoast Sitemap Scraper..."
echo ""

# Kích hoạt virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Tạo virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Cài đặt dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Chạy scraper
echo ""
echo "▶️  Chạy scraper..."
echo ""
python sitemap_scraper.py

echo ""
echo "✅ Hoàn tất!"
