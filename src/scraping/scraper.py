import os
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from scraping.robots_utils import is_allowed, USER_AGENT
from utils.logger import logging

HEADERS = {
    "User-Agent": USER_AGENT
}

def save_raw_html(html: str, filename: str):
    os.makedirs("data/raw/html", exist_ok=True)
    with open(f"data/raw/html/{filename}", "w", encoding="utf-8") as f:
        f.write(html)

def save_scraped_json(data, filename: str):
    os.makedirs("data/raw/scraped", exist_ok=True)
    with open(f"data/raw/scraped/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def scrape_single_page(url: str, base_url: str):
    if not is_allowed(base_url, url):
        logging.warning(f"Scraping not allowed by robots.txt: {url}")
        return []

    try:
        logging.info(f"Scraping single page: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        save_raw_html(response.text, "single_page.html")

        soup = BeautifulSoup(response.text, "lxml")

        records = []

        # CHANGE THESE selectors to match your site
        items = soup.select(".card, .item, article, tr")

        for item in items:
            record = {
                "title": item.select_one(".title, h2, h3, td.name").get_text(strip=True)
                if item.select_one(".title, h2, h3, td.name") else "",
                "description": item.select_one(".description, p, td.description").get_text(strip=True)
                if item.select_one(".description, p, td.description") else "",
                "price_or_date": item.select_one(".price, .date, td.year, td.price").get_text(strip=True)
                if item.select_one(".price, .date, td.year, td.price") else "",
                "link": item.select_one("a")["href"]
                if item.select_one("a") and item.select_one("a").has_attr("href") else "",
                "source": url,
                "type": "scraped",
                "extraction_timestamp": datetime.utcnow().isoformat()
            }
            records.append(record)

        save_scraped_json(records, "single_page.json")
        time.sleep(1.5)
        return records

    except Exception as e:
        logging.error(f"Error scraping single page {url}: {e}")
        return []

def scrape_multi_page(url_template: str, base_url: str, start_page: int = 1, end_page: int = 3):
    all_records = []

    for page in range(start_page, end_page + 1):
        url = url_template.format(page=page)

        if not is_allowed(base_url, url):
            logging.warning(f"Blocked by robots.txt: {url}")
            continue

        try:
            logging.info(f"Scraping page {page}: {url}")
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            save_raw_html(response.text, f"page_{page}.html")

            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select(".card, .item, article, tr")

            page_records = []

            for item in items:
                record = {
                    "title": item.select_one(".title, h2, h3, td.name").get_text(strip=True)
                    if item.select_one(".title, h2, h3, td.name") else "",
                    "description": item.select_one(".description, p, td.description").get_text(strip=True)
                    if item.select_one(".description, p, td.description") else "",
                    "price_or_date": item.select_one(".price, .date, td.year, td.price").get_text(strip=True)
                    if item.select_one(".price, .date, td.year, td.price") else "",
                    "link": item.select_one("a")["href"]
                    if item.select_one("a") and item.select_one("a").has_attr("href") else "",
                    "source": url,
                    "type": "scraped",
                    "page": page,
                    "extraction_timestamp": datetime.utcnow().isoformat()
                }
                page_records.append(record)

            all_records.extend(page_records)
            time.sleep(1.5)

        except Exception as e:
            logging.error(f"Error scraping page {page}: {e}")

    save_scraped_json(all_records, "multi_page.json")
    return all_records