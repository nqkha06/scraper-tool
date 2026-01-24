import base64
from pydoc import text
from urllib import response
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time
import os
from math import ceil

from gpt_rewriter import GPTRewriter, RewriteConfig

IS_REWRITE_MODE = True

config = RewriteConfig(
    model="gpt-4.1-mini",
    temperature=0.7,
    top_p=0.9,
    max_output_tokens=2500,
)

def wp_original_image_simple(url: str) -> str:
    path = urlparse(url).path
    parts = path.rsplit('.', 1)

    name = parts[0]
    ext = parts[1]

    if '-' in name and name.split('-')[-1].count('x') == 1:
        name = '-'.join(name.split('-')[:-1])

    return url.replace(path, f"{name}.{ext}")

class YoastSitemapScraper:
    def __init__(self, base_url="https://liteapks.com"):
        self.base_url = base_url
        self.sitemap_url = f"{base_url}/sitemap.xml"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.articles_data = []
        
    def get_sitemap_urls(self):
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
                    print(f"Found: {loc.text}")
            
            return sitemap_urls
        except Exception as e:
            print(f"ERROR: {e}")
            return []
    
    def get_article_urls_from_sitemap(self, sitemap_url):
        """Lấy tất cả URLs bài viết từ một sitemap"""
        print(f"\n📄 Đang phân tích sitemap: {sitemap_url}")
        try:
            response = requests.get(sitemap_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            urls = [
            # {"url": "https://liteapks.com/ark-ultimate-mobile-edition.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/fl-studio-mobile.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/alien-invasion.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/my-supermarket-simulator-3d.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/spider-fighter-3.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/mall-fast-food-simulator-3d.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/state-io.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/pk-xd.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/bitlife-3.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/the-schedule-i-project.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/crowd-evolution.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/truck-masters-india.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/good-pizza-great-pizza.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/sakura-school-simulator.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/the-battle-cats.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            # {"url": "https://liteapks.com/kinemaster-app.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            {"url": "https://liteapks.com/merge-fellas.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            {"url": "https://liteapks.com/nightclub-tycoon-idle-manager.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            {"url": "https://liteapks.com/beach-buggy-racing-2.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            {"url": "https://liteapks.com/frag-pro-shooter.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            {"url": "https://liteapks.com/f-class-adventurer.html", "lastmod": "2026-01-01T12:00:00+00:00"},
            {"url": "https://liteapks.com/pokemon-go.html", "lastmod": "2026-01-01T12:00:00+00:00"},


        ]


            # for url in root.findall('.//ns:url', namespace):
            #     loc = url.find('ns:loc', namespace)
            #     lastmod = url.find('ns:lastmod', namespace)
                
            #     if loc is not None:
            #         url_data = {
            #             'url': loc.text,
            #             'lastmod': lastmod.text if lastmod is not None else None
            #         }
            #         urls.append(url_data)
            
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
            
            thumbnailUrl = ""

            for script in soup.find_all("script", type="application/ld+json"):
                if not script.string:
                    continue

                try:
                    data = json.loads(script.string)
                except Exception:
                    continue

                if isinstance(data, dict) and "@graph" in data:
                    for g in data["@graph"]:
                        thumb = g.get("thumbnailUrl")
                        if thumb:
                            thumbnailUrl = thumb
                            break

                if thumbnailUrl:
                    break

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

            poster = soup.find('meta', {'property': 'og:image'}).get('content', '') if soup.find('meta', {'property': 'og:image'}) else ''

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
                        
            # 5. RATING & REVIEWS
            rating = ""
            rating_count = ""
            
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
            download_link = []
            download_btn = soup.find('a', href=lambda x: x and '/download/' in str(x))
            if download_btn:
                download_link = self.get_download_link(urljoin(self.base_url, download_btn.get('href', '')))

            content = ""
            entry_content = soup.select_one("div>div.entry-content")
            if entry_content:
                content = entry_content.decode_contents().strip()
            
            # 10. HÌNH ẢNH

            slide_tag = soup.select_one(".overflow-auto.mb-3")
     
            images = []
            
            # Screenshots từ content
            if slide_tag:
                img_tags = slide_tag.find_all('img', src=True)
                for img in img_tags:
                    img_url = img.get('src', '')
                    if img_url and 'wp-content/uploads' in img_url:
                        full_url = urljoin(self.base_url, img_url)
                        if full_url not in images:
                            images.append(full_url)

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

            for i in range(len(images)):
                images[i] = wp_original_image_simple(images[i])

            wp_description_GP = description
            mod_info_GP = soup.select_one("#more-info-1>div").decode_contents().strip() if soup.select_one("#more-info-1>div") else ""
            whatnews = soup.select_one("section.mb-4>div.alert.alert-success").decode_contents().strip() if soup.select_one("section.mb-4>div.alert.alert-success") else ""

            if (IS_REWRITE_MODE):
                rewriter = GPTRewriter(config=config)
                print("  ✍️  Rewriting description [content]...")
                content = rewriter.rewrite_html(content)
                print("  ✍️  Rewriting wp_description_GP...")
                if wp_description_GP:
                    wp_description_GP = rewriter.rewrite_text(wp_description_GP)
                print("  ✍️  Rewriting mod info...")
                if mod_info_GP:
                    mod_info_GP = rewriter.rewrite_html(mod_info_GP)
                print("  ✍️  Rewriting what's new...")
                if whatnews:
                    whatnews = rewriter.rewrite_html(whatnews)
            

            article_data = {
                'title': title_text,
                'description': content,
                'thumbnail': thumbnailUrl,
                'slug': url.rstrip('.html').split('/')[-1],
                'category': {
                    'name': categories[0] if len(categories) > 0 else 'N/A',
                    'slug': categories[0].lower().replace(' ', '-') if len(categories) > 0 else 'n-a'
                },
                'subcategory': {
                    'name': categories[1] if len(categories) > 1 else 'N/A',
                    'slug': categories[1].lower().replace(' ', '-') if len(categories) > 1 else 'n-a'
                },
                'apktemplates': {
                    "wp_description_GP": wp_description_GP,
                    "wp_mod_info_GP": mod_info_GP,
                    "wp_whatnews_GP": whatnews,
                    "wp_title_GP": app_name,
                    "wp_version_GP": version,
                    "wp_developers_GP": publisher, #Publisher
                    "wp_sizes_GP": size,
                    "wp_GP_ID": "",
                    "wp_mods": mod_info,
                    "avg_rating": rating,
                    "total_votes": rating_count,
                    "repeatable_download_link": [
                        i for i in download_link
                    ],
                    "ss_images": [{"ss_url": img} for img in images],

                    "wp_poster_GP": poster
                },
                'scraped_at': datetime.now().isoformat()
            }
            
            return article_data
            
        except Exception as e:
            print(f"  ❌ Lỗi khi scrape {url}: {e}")
            return None
    
    def scrape_all(self, max_articles=None, delay=1, sitemap_urls=None):
        """Thu thập tất cả bài viết từ sitemap"""
        print("🚀 Bắt đầu thu thập dữ liệu\n")
        
        # Nếu không cung cấp sitemap URLs, lấy từ sitemap chính
        if sitemap_urls is None:
            # sitemap_urls = self.get_sitemap_urls()
            sitemap_urls = [
                    f"{self.base_url}/post-sitemap1.xml",
                ]

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
    
    def save_to_json(
        self,
        base_filename="articles_data",
        chunk_size=50,
        output_dir="23-01"
    ):

        if not self.articles_data:
            print("⚠️  Không có dữ liệu để lưu!")
            return

        # thư mục output
        base_path = os.path.join(os.path.dirname(__file__), output_dir)
        os.makedirs(base_path, exist_ok=True)

        total_items = len(self.articles_data)
        total_chunks = ceil(total_items / chunk_size)

        for index in range(total_chunks):
            start = index * chunk_size
            end = start + chunk_size
            chunk_items = self.articles_data[start:end]

            payload = {
                "info": {
                    "theme_name": "modyolo",
                    "theme_author": "admin",
                    "theme_developer": "Sathish & Sahil",
                    "theme_buy_link": "https://apkfindy.com/product/modyolo",
                    "website": "https://apkfindy.com",
                    "created": "2026-01-01"
                },
                "posts": chunk_items
            }

            filename = f"{base_filename}_part_{index + 1}.json"
            filepath = os.path.join(base_path, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

            print(f"SAVED: {filepath} ({len(chunk_items)} articles)")

    def get_download_link(self, url):
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
            
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []

        accordion = soup.find(id='accordion-versions')

        if not accordion:
            return []
            accordion = soup.find("article")
        else:
            for item in accordion.select('.border.rounded.mb-2'):
                # # NAME
                # name_tag = item.select_one('div.collapse a>span>span')
                # name = name_tag.get_text(strip=True) if name_tag else ""

                # DOWNLOAD BUTTON
                download_btn = item.select_one('a[href*="/download/"]')
                if not download_btn:
                    continue

                url = urljoin(self.base_url, download_btn.get('href', ''))

                # VERSION (Mod Menu / empty cũng không crash)
                collapse = item.select_one('a.collapsed')
                version, info = [x.strip() for x in collapse.get_text(strip=True).split("-", 1)]
                version = version.lstrip("v")

                # SIZE
                size_tag = item.select_one('span.ml-auto')
                size = size_tag.get_text(strip=True) if size_tag else ""

                results.append({
                    'download_name': "APK",
                    'download_url': url,
                    'download_version': version,
                    'download_size': size,
                    'download_mod_info': info
                })

        for i in results:
            url = i['download_url']

            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=15,
                    allow_redirects=True
                )
                response.raise_for_status()
            except Exception:
                i['download_url'] = url  # fallback

                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            link_tag = soup.find(id='download-loaded-link')
            if link_tag and link_tag.has_attr('data-href'):
                i['download_url'] = base64.b64decode(link_tag['data-href']).decode('utf-8')
            else:
                i['download_url'] = response.url

        return results

def main():
    """Hàm chính"""
    print("="*60)
    print("   START SCRAPING from liteapks.com   ")
    print("="*60 + "\n")
    
    scraper = YoastSitemapScraper()
 
    scraper.scrape_all(max_articles=500, delay=1)
    
    # Lưu kết quả
    if scraper.articles_data:
        # scraper.save_to_csv('liteapks_articles.csv')
        scraper.save_to_json('liteapks_articles.json')

if __name__ == "__main__":
    main()
