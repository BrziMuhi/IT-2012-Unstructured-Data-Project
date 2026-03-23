import requests
import json
import logging
from pathlib import Path

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_cities():
    url = "https://geodb-free-service.wirefreethought.com/v1/geo/cities?limit=5"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        output_folder = Path("data/raw/cities")
        output_folder.mkdir(parents=True, exist_ok=True)

        output_file = output_folder / "cities.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logging.info(f"Successfully fetched and saved data to {output_file}")
        print(f"Data saved to {output_file}")

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        print("Error while fetching API data.")

if __name__ == "__main__":
    fetch_cities()