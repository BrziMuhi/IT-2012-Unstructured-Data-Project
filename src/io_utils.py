import json
import csv
import logging
from pathlib import Path


def setup_logging(log_file: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def read_json(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"Successfully read JSON file: {file_path}")
            return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error while reading JSON {file_path}: {e}")


def read_text(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            logging.info(f"Successfully read text file: {file_path}")
            return text
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error while reading text {file_path}: {e}")


def read_csv(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            logging.info(f"Successfully read CSV file: {file_path}")
            return rows
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error while reading CSV {file_path}: {e}")


