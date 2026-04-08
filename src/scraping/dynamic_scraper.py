import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from utils.logger import logging
from scraping.robots_utils import USER_AGENT

HEADERS = {
    "User-Agent": USER_AGENT
}

def scrape_json_api(api_url: str):
    try:
        logging.info(f"Scraping JSON API: {api_url}")
        response = requests.get(api_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()

        records = []
        if isinstance(data, list):
            for item in data:
                item["type"] = "json_api"
                item["source"] = api_url
                item["extraction_timestamp"] = datetime.utcnow().isoformat()
                records.append(item)
        else:
            data["type"] = "json_api"
            data["source"] = api_url
            data["extraction_timestamp"] = datetime.utcnow().isoformat()
            records.append(data)

        return records

    except Exception as e:
        logging.error(f"JSON API scraping failed: {e}")
        return []

def scrape_with_selenium(url: str):
    try:
        logging.info(f"Scraping dynamic page with Selenium: {url}")

        options = Options()
        options.add_argument("--headless")
        options.add_argument(f"user-agent={USER_AGENT}")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        cards = driver.find_elements(By.CSS_SELECTOR, ".card, .item, article, tr")
        records = []

        for card in cards:
            record = {
                "text": card.text.strip(),
                "source": url,
                "type": "selenium_dynamic",
                "extraction_timestamp": datetime.utcnow().isoformat()
            }
            records.append(record)

        driver.quit()
        return records

    except Exception as e:
        logging.error(f"Selenium scraping failed: {e}")
        return []