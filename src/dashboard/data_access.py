import os
from pathlib import Path

import pandas as pd
from pymongo import MongoClient


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_CANDIDATES = [
    PROJECT_ROOT / "data" / "processed" / "cleaned" / "cleaned_data.csv",
    PROJECT_ROOT / "data" / "processed" / "cleaned" / "clean.csv",
    PROJECT_ROOT / "processed" / "cleaned" / "cleaned_data.csv",
    PROJECT_ROOT / "processed" / "cleaned" / "clean.csv",
]

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "movie_analytics")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "movies")


def _find_csv_path():
    for path in CSV_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("No cleaned movie CSV found in data/processed/")


def _normalize_columns(df):
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

    df = df[df["year"] > 0]

    return df


def load_from_csv():
    csv_path = _find_csv_path()
    df = pd.read_csv(csv_path)
    return _normalize_columns(df)


def load_from_mongo():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")

    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION]

    records = list(collection.find({}, {"_id": 0}))

    if not records:
        raise ValueError("MongoDB collection is empty.")

    df = pd.DataFrame(records)
    return _normalize_columns(df)


def load_movies():
    try:
        return load_from_mongo()
    except Exception:
        return load_from_csv()


def get_genres():
    df = load_movies()
    genres = sorted(df["genre"].dropna().astype(str).unique().tolist())
    return ["All"] + genres


def get_year_range():
    df = load_movies()

    if df.empty:
        return 1900, 2025

    return int(df["year"].min()), int(df["year"].max())


def filter_movies(genre="All", year_range=None, search_text=""):
    df = load_movies()

    if genre and genre != "All":
        df = df[df["genre"].astype(str) == genre]

    if year_range and len(year_range) == 2:
        start_year, end_year = year_range
        df = df[(df["year"] >= start_year) & (df["year"] <= end_year)]

    if search_text:
        search_text = search_text.lower().strip()
        df = df[df["title"].astype(str).str.lower().str.contains(search_text, na=False)]

    return df