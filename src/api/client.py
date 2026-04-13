import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")


def fetch_places(pages=3):
    all_data = []

    if not API_KEY:
        print("Missing GEOAPIFY_API_KEY in .env")
        return all_data

    os.makedirs("data/raw/api", exist_ok=True)

    for page in range(1, pages + 1):
        url = "https://api.geoapify.com/v2/places"
        params = {
            "categories": "tourism.sights",
            "filter": "circle:18.4131,43.8563,5000",
            "limit": 10,
            "offset": (page - 1) * 10,
            "apiKey": API_KEY
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            all_data.extend(data.get("features", []))

            with open(f"data/raw/api/page_{page}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Saved page {page}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {page}: {e}")

    return all_data


def fetch_places_with_images(pages=3):
    all_data = []

    if not API_KEY:
        print("Missing GEOAPIFY_API_KEY in .env")
        return all_data

    for page in range(1, pages + 1):
        url = "https://api.geoapify.com/v2/places"
        params = {
            "categories": "tourism.sights",
            "filter": "circle:18.4131,43.8563,5000",
            "limit": 10,
            "offset": (page - 1) * 10,
            "apiKey": API_KEY
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for feature in data.get("features", []):
                props = feature.get("properties", {})

                image_url = None

                if "image" in props:
                    image_url = props["image"]
                elif "datasource" in props and "raw" in props["datasource"]:
                    raw = props["datasource"]["raw"]
                    image_url = raw.get("image") or raw.get("image_url")

                if image_url:
                    all_data.append({
                        "name": props.get("name"),
                        "image_url": image_url
                    })

        except requests.exceptions.RequestException as e:
            print(f"Request failed on page {page}: {e}")

    return all_data


if __name__ == "__main__":
    places = fetch_places(3)
    print(f"Fetched: {len(places)}")

    images = fetch_places_with_images(3)
    print(f"Found images: {len(images)}")