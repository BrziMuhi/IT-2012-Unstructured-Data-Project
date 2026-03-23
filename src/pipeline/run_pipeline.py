import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from utils.logger import logging
from api.client import fetch_places
from storage.mongo import save_to_mongo
from storage.s3 import upload_file_to_s3


def run_pipeline():
    logging.info("Pipeline started")

    places = fetch_places(3)

    for place in places:
        save_to_mongo(place, "geoapify_api")

    for page in range(1, 4):
        file_path = f"data/raw/api/page_{page}.json"
        file_name = f"page_{page}.json"
        upload_file_to_s3(file_path, file_name)

    logging.info("Pipeline finished successfully")


if __name__ == "__main__":
    run_pipeline()