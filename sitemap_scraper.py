#!/usr/bin/env python3
"""
Công cụ thu thập dữ liệu từ Yoast Sitemap
Tool to scrape data from Yoast sitemap articles
"""

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
import json
from datetime import datetime
from urllib.parse import urljoin
import time
import os

class YoastSitemapScraper:
    def __init__(self, base_url="https://liteapks.com"):
        self.base_url = base_url
        self.sitemap_url = f"{base_url}/sitemap.xml"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.articles_data = []
        
    def get_sitemap_urls(self):
        """Lấy danh sách tất cả các sitemap URLs"""
        print(f"📡 Đang tải sitemap chính từ: {self.sitemap_url}")
        try:
            response = requests.get(self.sitemap_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            sitemap_urls = []
            for sitemap in root.findall('.//ns:sitemap', namespace):
                loc = sitemap.find('ns:loc', namespace)
                if loc is not None and 'post-sitemap' in loc.text:
                    sitemap_urls.append(loc.text)
                    print(f"  ✓ Tìm thấy: {loc.text}")
            
            return sitemap_urls
        except Exception as e:
            print(f"❌ Lỗi khi tải sitemap: {e}")
            return []
    
    def get_article_urls_from_sitemap(self, sitemap_url):
        """Lấy tất cả URLs bài viết từ một sitemap"""
        print(f"\n📄 Đang phân tích sitemap: {sitemap_url}")
        try:
            response = requests.get(sitemap_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            urls = []
            for url in root.findall('.//ns:url', namespace):
                loc = url.find('ns:loc', namespace)
                lastmod = url.find('ns:lastmod', namespace)
                
                if loc is not None:
                    url_data = {
                        'url': loc.text,
                        'lastmod': lastmod.text if lastmod is not None else None
                    }
                    urls.append(url_data)
            
            print(f"  ✓ Tìm thấy {len(urls)} bài viết")
            return urls
        except Exception as e:
            print(f"  ❌ Lỗi: {e}")
            return []
    
    def scrape_article(self, url):
        """Thu thập dữ liệu từ một bài viết - Phiên bản tối ưu"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 1. METADATA CƠ BẢN
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else "N/A"
            
            # Meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            description = meta_desc.get('content', 'N/A') if meta_desc else "N/A"
            
            # 2. JSON-LD SCHEMA DATA
            schema_data = {}
            json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
            for script in json_ld_scripts:
                try:
                    import json as json_module
                    data = json_module.loads(script.string)
                    if isinstance(data, dict):
                        if data.get('@type') == 'SoftwareApplication':
                            schema_data = data
                            break
                except:
                    pass
            
            # 3. THÔNG TIN TỪ BẢNG (TABLE)
            app_name = schema_data.get('name', 'N/A')
            publisher = "N/A"
            genre = "N/A"
            size = "N/A"
            version = schema_data.get('softwareVersion', 'N/A')
            mod_info = "N/A"
            google_play_link = "N/A"
            
            info_table = soup.find('table', class_='table')
            if info_table:
                rows = info_table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['th', 'td'])
                    if len(cells) == 2:
                        key = cells[0].get_text(strip=True).lower()
                        
                        if 'app name' in key:
                            app_name = cells[1].get_text(strip=True)
                        elif 'publisher' in key:
                            # Tìm link trong cell
                            link = cells[1].find('a')
                            publisher = link.get_text(strip=True) if link else cells[1].get_text(strip=True)
                        elif 'genre' in key:
                            link = cells[1].find('a')
                            genre = link.get_text(strip=True) if link else cells[1].get_text(strip=True)
                        elif 'size' in key:
                            size = cells[1].get_text(strip=True)
                        elif 'latest version' in key or 'version' in key:
                            version = cells[1].get_text(strip=True)
                        elif 'mod info' in key:
                            mod_info = cells[1].get_text(strip=True)
                        elif 'get it on' in key:
                            play_link = cells[1].find('a')
                            if play_link:
                                google_play_link = play_link.get('href', 'N/A')
            
            # 4. MOD INFO CHI TIẾT (từ accordion)
            mod_details = []
            accordion = soup.find('div', id='accordion-more-info')
            if accordion:
                mod_content = accordion.find('div', class_='collapse')
                if mod_content:
                    mod_list = mod_content.find_all('li')
                    for li in mod_list:
                        mod_text = li.get_text(strip=True)
                        if mod_text:
                            mod_details.append(mod_text)
            
            mod_info_detailed = '; '.join(mod_details) if mod_details else mod_info
            
            # 5. RATING & REVIEWS
            rating = "N/A"
            rating_count = "N/A"
            rating_div = soup.find('div', class_='rating')
            if rating_div:
                rating = rating_div.get('data-rateyo-rating', 'N/A')
            
            # Từ schema
            if 'aggregateRating' in schema_data:
                rating = schema_data['aggregateRating'].get('ratingValue', rating)
                rating_count = schema_data['aggregateRating'].get('ratingCount', rating_count)
            
            # Từ text
            rating_text = soup.find('span', string=lambda x: x and '/5' in str(x))
            if rating_text:
                rating_parts = rating_text.get_text(strip=True).split()
                if len(rating_parts) > 0:
                    rating = rating_parts[0].replace('/5', '')
                if '(' in rating_text.get_text():
                    import re
                    votes = re.search(r'\((\d+)\s*votes?\)', rating_text.get_text())
                    if votes:
                        rating_count = votes.group(1)
            
            # 6. AUTHOR & DATES
            author = "N/A"
            author_meta = soup.find('meta', {'name': 'author'})
            if author_meta:
                author = author_meta.get('content', 'N/A')
            
            published_time = "N/A"
            modified_time = "N/A"
            pub_meta = soup.find('meta', {'property': 'article:published_time'})
            if pub_meta:
                published_time = pub_meta.get('content', 'N/A')
            
            mod_meta = soup.find('meta', {'property': 'article:modified_time'})
            if mod_meta:
                modified_time = mod_meta.get('content', 'N/A')
            
            # 7. BREADCRUMB / CATEGORIES
            categories = []
            breadcrumb = soup.find('ul', id='breadcrumb')
            if breadcrumb:
                cat_items = breadcrumb.find_all('li', class_='item-cat')
                for item in cat_items:
                    link = item.find('a')
                    if link:
                        categories.append(link.get_text(strip=True))
            
            category_path = ' > '.join(categories) if categories else genre
            
            # 8. DOWNLOAD LINK
            download_link = "N/A"
            download_btn = soup.find('a', href=lambda x: x and '/download/' in str(x))
            if download_btn:
                download_link = urljoin(self.base_url, download_btn.get('href', ''))
            
            # 9. NỘI DUNG BÀI VIẾT
            content = "N/A"
            entry_content = soup.find('div', class_='entry-content')
            if entry_content:
                # Lấy tất cả paragraphs
                paragraphs = entry_content.find_all('p')
                content_parts = []
                for p in paragraphs[:3]:  # Lấy 3 đoạn đầu
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:  # Bỏ qua đoạn quá ngắn
                        content_parts.append(text)
                
                content = ' '.join(content_parts)
                if len(content) > 800:
                    content = content[:800] + "..."
            
            # 10. HÌNH ẢNH
            images = []
            
            # Main featured image
            main_img = soup.find('meta', {'property': 'og:image'})
            if main_img:
                images.append(main_img.get('content', ''))
            
            # Screenshots từ content
            if entry_content:
                img_tags = entry_content.find_all('img', src=True)
                for img in img_tags:
                    img_url = img.get('src', '')
                    if img_url and 'wp-content/uploads' in img_url:
                        full_url = urljoin(self.base_url, img_url)
                        if full_url not in images:
                            images.append(full_url)
            
            # Giới hạn số ảnh
            images = images[:10]
            
            # 11. OPERATING SYSTEM
            operating_system = schema_data.get('operatingSystem', 'Android')
            
            # 12. PRICE
            price = "Free"
            if 'offers' in schema_data:
                price_val = schema_data['offers'].get('price', '0')
                currency = schema_data['offers'].get('priceCurrency', 'USD')
                if price_val == '0' or price_val == 0:
                    price = "Free"
                else:
                    price = f"{price_val} {currency}"
            
            # TẠO DICTIONARY KẾT QUẢ
            article_data = {
                'url': url,
                'title': title_text,
                'description': description,
                'app_name': app_name,
                'publisher': publisher,
                'author': author,
                'genre': genre,
                'categories': category_path,
                'size': size,
                'version': version,
                'operating_system': operating_system,
                'price': price,
                'mod_info': mod_info_detailed,
                'rating': str(rating),
                'rating_count': str(rating_count),
                'google_play_link': google_play_link,
                'download_link': download_link,
                'published_time': published_time,
                'modified_time': modified_time,
                'content': content,
                'images': '|'.join(images),  # Phân cách bằng |
                'image_count': len(images),
                'scraped_at': datetime.now().isoformat()
            }
            
            return article_data
            
        except Exception as e:
            print(f"  ❌ Lỗi khi scrape {url}: {e}")
            return None
    
    def scrape_all(self, max_articles=None, delay=1, sitemap_urls=None):
        """Thu thập tất cả bài viết từ sitemap"""
        print("🚀 Bắt đầu thu thập dữ liệu từ Yoast Sitemap\n")
        
        # Nếu không cung cấp sitemap URLs, lấy từ sitemap chính
        if sitemap_urls is None:
            sitemap_urls = self.get_sitemap_urls()
            
            if not sitemap_urls:
                print("⚠️  Không tìm thấy sitemap từ trang chính.")
                print("💡 Sử dụng danh sách sitemap mặc định...")
                # Danh sách sitemap backup
                sitemap_urls = [
                    f"{self.base_url}/post-sitemap.xml",
                    f"{self.base_url}/post-sitemap2.xml",
                    f"{self.base_url}/post-sitemap3.xml",
                ]
        
        # Lấy tất cả URLs bài viết
        all_article_urls = []
        for sitemap_url in sitemap_urls:
            article_urls = self.get_article_urls_from_sitemap(sitemap_url)
            all_article_urls.extend(article_urls)
        
        print(f"\n📊 Tổng cộng: {len(all_article_urls)} bài viết")
        
        # Giới hạn số lượng nếu có
        if max_articles:
            all_article_urls = all_article_urls[:max_articles]
            print(f"⚠️  Giới hạn: Chỉ scrape {max_articles} bài viết đầu tiên")
        
        # Thu thập dữ liệu từng bài viết
        print(f"\n📥 Bắt đầu thu thập dữ liệu...\n")
        for idx, article in enumerate(all_article_urls, 1):
            print(f"[{idx}/{len(all_article_urls)}] Đang scrape: {article['url']}")
            
            article_data = self.scrape_article(article['url'])
            if article_data:
                article_data['lastmod'] = article['lastmod']
                self.articles_data.append(article_data)
                print(f"  ✅ Thành công: {article_data['title']}")
            
            # Delay để tránh bị block
            time.sleep(delay)
        
        print(f"\n✨ Hoàn thành! Đã thu thập {len(self.articles_data)} bài viết")
    
    def save_to_csv(self, filename='articles_data.csv'):
        """Lưu dữ liệu vào file CSV"""
        if not self.articles_data:
            print("⚠️  Không có dữ liệu để lưu!")
            return
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = self.articles_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.articles_data)
        
        print(f"💾 Đã lưu vào: {filepath}")
    
    def save_to_json(self, filename='articles_data.json'):
        """Lưu dữ liệu vào file JSON"""
        if not self.articles_data:
            print("⚠️  Không có dữ liệu để lưu!")
            return
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.articles_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Đã lưu vào: {filepath}")


def main():
    """Hàm chính"""
    print("="*60)
    print("   CÔNG CỤ THU THẬP DỮ LIỆU YOAST SITEMAP")
    print("   Liteapks.com Scraper Tool - PHIÊN BẢN TỐI ƯU")
    print("="*60 + "\n")
    
    scraper = YoastSitemapScraper()
    
    # Thu thập dữ liệu (giới hạn 50 bài đầu tiên để test)
    # Bỏ max_articles=50 để scrape tất cả
    scraper.scrape_all(max_articles=50, delay=1)
    
    # Lưu kết quả
    if scraper.articles_data:
        scraper.save_to_csv('liteapks_articles.csv')
        scraper.save_to_json('liteapks_articles.json')
        
        print("\n📈 Thống kê:")
        print(f"  - Tổng số bài viết: {len(scraper.articles_data)}")
        print(f"  - Định dạng lưu trữ: CSV và JSON")
        print(f"  - Số trường dữ liệu: 25+ trường/bài viết")
        
        # Hiển thị 1 bài mẫu
        if len(scraper.articles_data) > 0:
            print("\n📄 Bài viết mẫu (đầu tiên):")
            sample = scraper.articles_data[0]
            print(f"  • Title: {sample['title'][:60]}...")
            print(f"  • App: {sample['app_name']}")
            print(f"  • Rating: {sample['rating']}/5 ({sample['rating_count']} votes)")
            print(f"  • Version: {sample['version']}")
            print(f"  • Size: {sample['size']}")
            print(f"  • MOD: {sample['mod_info'][:50]}...")
            print(f"  • Images: {sample['image_count']} ảnh")


if __name__ == "__main__":
    main()
