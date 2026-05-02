import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logger import logging

from api.client import fetch_places
from storage.mongo import save_to_mongo
from storage.s3 import upload_file_to_s3

from scraping.scraper import scrape_single_page, scrape_multi_page
from scraping.dynamic_scraper import scrape_json_api, scrape_with_selenium

from ocr.ocr_utils import ocr_image, ocr_scanned_pdf

from analytics.numpy_ops import run_numpy_operations
from analytics.data_loader import run_data_loader, load_csv
from analytics.explorer import run_exploration
from analytics.selector import run_selector
from analytics.regex_ops import run_regex_ops
from analytics.quality_report import run_quality_report

from cleaning.clean_pipeline import run_cleaning_pipeline


def run_pipeline():
    logging.info("Pipeline started")

    try:
        # 1. API data
        logging.info("Fetching API data...")
        places = fetch_places(3)

        logging.info("Saving API data to MongoDB...")
        for place in places:
            save_to_mongo(place, "geoapify_api")

        # logging.info("Uploading raw JSON files to S3...")
        # for page in range(1, 4):
        #     file_path = f"data/raw/api/page_{page}.json"
        #     file_name = f"page_{page}.json"
        #     upload_file_to_s3(file_path, file_name)

        # 2. Single-page scraping
        logging.info("Starting single-page scraping...")
        single_page_data = scrape_single_page(
            "https://books.toscrape.com/",
            "https://books.toscrape.com/"
        )

        if single_page_data:
            save_to_mongo(single_page_data, "scraped_data")

        # 3. Multi-page scraping
        logging.info("Starting multi-page scraping...")
        multi_page_data = scrape_multi_page(
            "https://books.toscrape.com/catalogue/page-{page}.html",
            "https://books.toscrape.com",
            1,
            3
        )

        if multi_page_data:
            save_to_mongo(multi_page_data, "scraped_data")

        # 4. JSON API scraping
        logging.info("Starting JSON API scraping...")
        json_api_data = scrape_json_api("https://jsonplaceholder.typicode.com/posts")

        if json_api_data:
            save_to_mongo(json_api_data, "scraped_data")

        # 5. Selenium fallback
        logging.info("Starting Selenium scraping...")
        selenium_data = scrape_with_selenium("https://quotes.toscrape.com/js/")

        if selenium_data:
            save_to_mongo(selenium_data, "scraped_data")

        # 6. OCR image
        image_path = "data/raw/images/test_scan.png"

        if os.path.exists(image_path):
            logging.info("Starting OCR on image...")
            image_result = ocr_image(image_path)

            if image_result:
                save_to_mongo(image_result, "ocr_data")

        # 7. OCR scanned PDF
        pdf_path = "data/raw/scanned/test_scan.pdf"

        if os.path.exists(pdf_path):
            logging.info("Starting OCR on scanned PDF...")
            pdf_results = ocr_scanned_pdf(pdf_path)

            if pdf_results:
                save_to_mongo(pdf_results, "ocr_data")

        # 8. Lab 8 analytics
        logging.info("Starting Lab 8 analytics")

        run_numpy_operations()
        run_data_loader()

        df = load_csv()

        run_exploration(df)
        run_selector()
        run_regex_ops()
        run_quality_report()

        # 9. Lab 9 cleaning
        logging.info("Starting Lab 9 cleaning pipeline")

        if df is not None and not df.empty:
            clean_df = run_cleaning_pipeline(df)
            logging.info(f"Cleaning completed. Cleaned rows: {len(clean_df)}")
        else:
            logging.warning("Skipping Lab 9 cleaning because dataframe is empty")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()