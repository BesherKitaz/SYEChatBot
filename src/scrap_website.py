import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

# ==== CONFIG ====
BASE_URL = "https://sites.google.com/sye-initiative.org/studentresources/"
DOMAIN_PREFIX = "/sye-initiative.org/studentresources/"
OUTPUT_DIR = "scraped_pages"
MAX_DEPTH = 15
# ================

# Ensure the folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_html_to_file(url: str, soup: BeautifulSoup, depth: int):
    """Save the parsed HTML to a .txt file (prettified)."""
    # Use a filesystem-safe filename based on the URL
    safe_name = quote(url.replace("https://", "").replace("/", "_"))
    filename = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    
    print("  " * depth + f"💾 Saved: {filename}")

def crawl(url, depth=0, visited=None):
    if visited is None:
        visited = set()

    if depth > MAX_DEPTH or url in visited:
        return

    print("  " * depth + f"→ Level {depth}: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("  " * depth + f"✗ Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    save_html_to_file(url, soup, depth)

    time.sleep(1)  # polite delay

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()

        # Follow only internal links
        if href.startswith(DOMAIN_PREFIX) or (
            href.startswith("/") and DOMAIN_PREFIX in href
        ):
            next_url = urljoin(BASE_URL, href)
            crawl(next_url, depth + 1, visited)

crawl(BASE_URL)
