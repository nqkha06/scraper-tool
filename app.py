from database.session import engine, get_conn
from sqlalchemy import text

import requests
import xml.etree.ElementTree as ET
from datetime import datetime

print(get_conn())
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
def get_article_urls_from_sitemap(sitemap_url):
    """Lấy tất cả URLs bài viết từ một sitemap"""
    print(f"\n📄 Đang phân tích sitemap: {sitemap_url}")
    try:
        response = requests.get(sitemap_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = []
        batch_data = []
        scraped_at = datetime.now()

        # Thu thập tất cả URLs trước
        for url in root.findall('.//ns:url', namespace):
            loc = url.find('ns:loc', namespace)
            lastmod = url.find('ns:lastmod', namespace)

            if loc is not None:
                url_data = {
                    'url': loc.text,
                    'lastmod': lastmod.text if lastmod is not None else None
                }
                batch_data.append({
                    "url": url_data["url"],
                    "modified_at": url_data["lastmod"],
                    "scraped_at": scraped_at
                })
                urls.append(url_data)
        
        # Batch insert - nhanh hơn nhiều
        if batch_data:
            with engine.connect() as conn:
                conn.execute(
                    text("INSERT INTO history (url, modified_at, scraped_at) VALUES (:url, :modified_at, :scraped_at)"),
                    batch_data
                )
                conn.commit()
        
        print(f"  ✓ Tìm thấy {len(urls)} bài viết")
        return urls
    except Exception as e:
        print(f"  ❌ Lỗi: {e}")
        return []

get_article_urls_from_sitemap("https://liteapks.com/post-sitemap9.xml")