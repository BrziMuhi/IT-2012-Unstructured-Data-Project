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

from analytics.db_connector import get_connection, create_places_table, populate_places, query_places
from analytics.pivot_builder import add_primary_category, category_year_pivot, city_category_crosstab
from analytics.aggregator import genre_summary, yearly_trends
from analytics.time_series import parse_dates, add_date_parts, monthly_time_series, yearly_time_series, add_rolling_averages
from analytics.insight_reporter import run_all_questions

from embeddings.chroma_store import add_movies_to_chroma


def run_lab10_analytics():
    logging.info("Starting Lab 10 analytics")

    cleaned_path = "processed/cleaned/cleaned_data.csv"
    analytics_dir = "processed/analytics"

    os.makedirs(analytics_dir, exist_ok=True)

    if not os.path.exists(cleaned_path):
        logging.warning(f"Skipping Lab 10 because cleaned CSV not found: {cleaned_path}")
        return

    df = pd.read_csv(cleaned_path)
    df = df.rename(columns={"_id": "place_id"})

    conn = get_connection(password="root")
    create_places_table(conn)
    populate_places(conn, cleaned_path)
    mysql_df = query_places(conn)
    conn.close()

    logging.info(f"MySQL rows loaded: {len(mysql_df)}")

    df = add_primary_category(df)

    genre_summary(df).to_csv(f"{analytics_dir}/category_analysis.csv", index=False)
    yearly_trends(df).to_csv(f"{analytics_dir}/yearly_trends.csv", index=False)

    category_year_pivot(df).to_csv(f"{analytics_dir}/pivot_category_year.csv")
    city_category_crosstab(df).to_csv(f"{analytics_dir}/city_category_crosstab.csv")

    df = parse_dates(df)
    df = add_date_parts(df)

    monthly = add_rolling_averages(monthly_time_series(df))
    monthly.to_csv(f"{analytics_dir}/monthly_time_series.csv", index=False)

    yearly_time_series(df).to_csv(f"{analytics_dir}/yearly_time_series.csv", index=False)

    run_all_questions(df)

    logging.info("Lab 10 analytics completed")


def run_pipeline():
    logging.info("Pipeline started")

    try:
        # Lab 1 API data
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

        # Lab 2 Single-page scraping
        logging.info("Starting single-page scraping...")
        single_page_data = scrape_single_page(
            "https://books.toscrape.com/",
            "https://books.toscrape.com/"
        )

        if single_page_data:
            save_to_mongo(single_page_data, "scraped_data")

        # Lab 3 Multi-page scraping
        logging.info("Starting multi-page scraping...")
        multi_page_data = scrape_multi_page(
            "https://books.toscrape.com/catalogue/page-{page}.html",
            "https://books.toscrape.com",
            1,
            3
        )

        if multi_page_data:
            save_to_mongo(multi_page_data, "scraped_data")

        # Lab 4 JSON API scraping
        logging.info("Starting JSON API scraping...")
        json_api_data = scrape_json_api("https://jsonplaceholder.typicode.com/posts")

        if json_api_data:
            save_to_mongo(json_api_data, "scraped_data")

        # Lab 5 Selenium fallback
        logging.info("Starting Selenium scraping...")
        selenium_data = scrape_with_selenium("https://quotes.toscrape.com/js/")

        if selenium_data:
            save_to_mongo(selenium_data, "scraped_data")

        # Lab 6 OCR image
        image_path = "data/raw/images/test_scan.png"

        if os.path.exists(image_path):
            logging.info("Starting OCR on image...")
            image_result = ocr_image(image_path)

            if image_result:
                save_to_mongo(image_result, "ocr_data")

        # Lab 7 OCR scanned PDF
        pdf_path = "data/raw/scanned/test_scan.pdf"

        if os.path.exists(pdf_path):
            logging.info("Starting OCR on scanned PDF...")
            pdf_results = ocr_scanned_pdf(pdf_path)

            if pdf_results:
                save_to_mongo(pdf_results, "ocr_data")

        # Lab 8 analytics
        logging.info("Starting Lab 8 analytics")

        run_numpy_operations()
        run_data_loader()

        df = load_csv()

        run_exploration(df)
        run_selector()
        run_regex_ops()
        run_quality_report()

        # Lab 9 cleaning
        logging.info("Starting Lab 9 cleaning pipeline")

        if df is not None and not df.empty:
            clean_df = run_cleaning_pipeline(df)
            logging.info(f"Cleaning completed. Cleaned rows: {len(clean_df)}")
        else:
            logging.warning("Skipping Lab 9 cleaning because dataframe is empty")

        # Lab 10 analytics
        run_lab10_analytics()

        # Lab 11 embeddings
        logging.info("Starting Lab 11 embeddings...")

        try:
            cleaned_path = "processed/cleaned/cleaned_data.csv"

            if os.path.exists(cleaned_path):
                df_embeddings = pd.read_csv(cleaned_path)
                add_movies_to_chroma(df_embeddings, reset=False)
                logging.info("Lab 11 embeddings completed successfully")
            else:
                logging.warning("Skipping Lab 11: cleaned dataset not found")

        except Exception as e:
            logging.error(f"Lab 11 embeddings failed: {e}")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()