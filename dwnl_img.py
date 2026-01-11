import json
import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

JSON_FILE = "/Users/qkha/Documents/tools/bug/11-01/liteapks_articles.json_part_1.json"
SAVE_ROOT = "images"
TIMEOUT = 20

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ImageBot/1.0)"
}

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def normalize_url(url: str, base: str = "https://liteapks.com"):
    if not url:
        return None
    if url.startswith("data:"):
        return None
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return urljoin(base, url)
    return url

def save_image(url: str):
    try:
        parsed = urlparse(url)
        if not parsed.netloc or not parsed.path:
            return

        local_path = os.path.join(
            SAVE_ROOT,
            parsed.netloc,
            parsed.path.lstrip("/")
        )

        ensure_dir(os.path.dirname(local_path))

        if os.path.exists(local_path):
            return

        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        r.raise_for_status()

        if int(r.headers.get("Content-Length", 0)) == 0:
            return

        with open(local_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

        print(f"✔ {url}")

    except Exception as e:
        print(f"✘ {url} | {e}")

def extract_images_from_description(html: str):
    soup = BeautifulSoup(html, "html.parser")
    urls = set()

    for img in soup.find_all("img"):
        for attr in ["src", "data-src", "data-lazy-src"]:
            u = img.get(attr)
            u = normalize_url(u)
            if u:
                urls.add(u)

        # srcset
        srcset = img.get("srcset")
        if srcset:
            for part in srcset.split(","):
                u = part.strip().split(" ")[0]
                u = normalize_url(u)
                if u:
                    urls.add(u)

    return list(urls)

def process_json():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])

    for post in posts:
        # DESCRIPTION
        desc = post.get("description", "")
        for img_url in extract_images_from_description(desc):
            save_image(img_url)

        # SS_IMAGES
        ss_images = post.get("apktemplates", {}).get("ss_images", [])
        for item in ss_images:
            img_url = normalize_url(item.get("ss_url"))
            if img_url:
                save_image(img_url)

if __name__ == "__main__":
    process_json()
