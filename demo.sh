#!/bin/bash
# Demo script - Scrape và export sang định dạng tùy chỉnh

echo "============================================================"
echo "   DEMO: SCRAPE & EXPORT ĐỊNH DẠNG TÙY CHỈNH"
echo "============================================================"
echo ""

# Activate virtual environment
echo "🔧 Kích hoạt virtual environment..."
source venv/bin/activate

# Scrape 10 bài để demo nhanh
echo ""
echo "📥 Scraping 10 bài viết để demo..."
python -c "
from sitemap_scraper import YoastSitemapScraper
from export_custom_format import export_to_custom_format

# Scrape
scraper = YoastSitemapScraper()
scraper.scrape_all(max_articles=10, delay=0.5)

# Save
scraper.save_to_json('demo_articles.json')

# Export custom format
if scraper.articles_data:
    config = {
        'theme_name': 'demo_theme',
        'website': 'https://liteapks.com'
    }
    
    export_to_custom_format(
        scraper.articles_data,
        output_prefix='demo_custom',
        posts_per_file=5,  # Chia làm 2 file
        config=config
    )
"

echo ""
echo "============================================================"
echo "✅ DEMO HOÀN TẤT!"
echo "============================================================"
echo ""
echo "📁 Files đã tạo:"
ls -lh demo_*.json
echo ""
echo "💡 Xem nội dung:"
echo "   cat demo_custom_1.json | jq '.info'"
echo "   cat demo_custom_1.json | jq '.posts[0].title'"
echo ""
