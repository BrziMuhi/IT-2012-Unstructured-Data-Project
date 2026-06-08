import os
from pathlib import Path

import pandas as pd
from pymongo import MongoClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_CANDIDATES = [
    PROJECT_ROOT / "data" / "processed" / "cleaned" / "cleaned_data.csv",
    PROJECT_ROOT / "data" / "processed" / "cleaned" / "clean.csv",
    PROJECT_ROOT / "processed" / "cleaned" / "cleaned_data.csv",
    PROJECT_ROOT / "processed" / "cleaned" / "clean.csv",
]

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "movie_analytics")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "movies")


def find_csv_path():
    for path in CSV_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("No cleaned CSV file found in data/processed/")


def normalize_columns(df):
    df = df.copy()
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    if "title" not in df.columns and "name" in df.columns:
        df["title"] = df["name"]

    if "title" not in df.columns:
        df["title"] = "Unknown"

    if "categories" in df.columns:
        df["genre"] = df["categories"].fillna("Unknown").astype(str).apply(
            lambda x: x.split(",")[0].strip() if x else "Unknown"
        )
    elif "category" in df.columns:
        df["genre"] = df["category"].fillna("Unknown").astype(str)
    elif "genre" not in df.columns:
        df["genre"] = "Unknown"

    if "timestamp_year" in df.columns:
        df["year"] = pd.to_numeric(df["timestamp_year"], errors="coerce").fillna(0).astype(int)
    elif "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)
    else:
        df["year"] = 0

    if "city" not in df.columns:
        df["city"] = "Unknown"

    if "country" not in df.columns:
        df["country"] = "Unknown"

    if "website" in df.columns:
        df["rating"] = df["website"].fillna("").astype(str).apply(lambda x: 1 if x.strip() else 0)
    else:
        df["rating"] = 0

    if "longitude" not in df.columns:
        df["longitude"] = 0

    if "latitude" not in df.columns:
        df["latitude"] = 0

    df["title"] = df["title"].fillna("Unknown").astype(str)
    df["genre"] = df["genre"].fillna("Unknown").astype(str)
    df["city"] = df["city"].fillna("Unknown").astype(str)
    df["country"] = df["country"].fillna("Unknown").astype(str)

    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce").fillna(0)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce").fillna(0)

    df["revenue"] = 1
    df["budget"] = 1

    return df


def main():
    csv_path = find_csv_path()
    df = pd.read_csv(csv_path)
    df = normalize_columns(df)

    records = df.to_dict("records")

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION]

    collection.delete_many({})

    if records:
        collection.insert_many(records)

    collection.create_index("genre")
    collection.create_index("year")
    collection.create_index("title")

    print(f"Seeded {len(records)} records into {MONGO_DB_NAME}.{MONGO_COLLECTION}")


if __name__ == "__main__":
    main()