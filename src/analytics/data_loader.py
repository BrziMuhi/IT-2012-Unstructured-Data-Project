import os
import pandas as pd
from pymongo import MongoClient
import ast


MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "tourism_pipeline"
COLLECTION_NAME = "raw_places"

OUTPUT_DIR = "processed/analytics"
CSV_PATH = f"{OUTPUT_DIR}/clean_data.csv"


def load_from_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    data = list(collection.find())
    df = pd.DataFrame(data)

    if "_id" in df.columns:
        df["_id"] = df["_id"].astype(str)

    print("Loaded from MongoDB")
    print("Shape:", df.shape)

    return df


def flatten_data_column(df):
    rows = []

    for _, row in df.iterrows():
        raw_data = row.get("data")

        if isinstance(raw_data, dict):
            data_items = [raw_data]
        elif isinstance(raw_data, list):
            data_items = raw_data
        else:
            try:
                parsed = ast.literal_eval(str(raw_data))
                if isinstance(parsed, list):
                    data_items = parsed
                elif isinstance(parsed, dict):
                    data_items = [parsed]
                else:
                    data_items = [{}]
            except Exception:
                data_items = [{}]

        for data in data_items:
            properties = data.get("properties", {})
            geometry = data.get("geometry", {})
            coordinates = geometry.get("coordinates", [None, None])

            rows.append({
                "_id": row.get("_id"),
                "source": row.get("source"),
                "timestamp": row.get("timestamp"),
                "name": properties.get("name"),
                "city": properties.get("city"),
                "country": properties.get("country"),
                "postcode": properties.get("postcode"),
                "street": properties.get("street"),
                "categories": ", ".join(properties.get("categories", [])) if isinstance(properties.get("categories"), list) else properties.get("categories"),
                "longitude": coordinates[0] if coordinates and len(coordinates) > 0 else None,
                "latitude": coordinates[1] if coordinates and len(coordinates) > 1 else None,
                "website": properties.get("website"),
                "formatted_address": properties.get("formatted")
            })

    flat_df = pd.DataFrame(rows)

    print("Flattened data column")
    print("New shape:", flat_df.shape)
    print(flat_df.head())

    return flat_df


def save_to_csv(df, path=CSV_PATH):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved CSV to {path}")


def load_csv(path=CSV_PATH):
    df = pd.read_csv(path)
    print("Loaded CSV")
    print("Shape:", df.shape)
    return df


def process_csv_in_chunks(path=CSV_PATH, chunksize=1000):
    total_sum = 0
    total_count = 0

    for chunk in pd.read_csv(path, chunksize=chunksize):
        if "latitude" in chunk.columns:
            total_sum += chunk["latitude"].sum()
            total_count += chunk["latitude"].count()

    if total_count == 0:
        print("No numeric column found for mean")
        return None

    global_mean = total_sum / total_count
    print("Global mean latitude:", global_mean)

    return global_mean


def process_chunks_per_language(path=CSV_PATH, chunksize=1000):
    stats = {}

    for chunk in pd.read_csv(path, chunksize=chunksize):
        if "city" not in chunk.columns:
            print("No city column found")
            return {}

        counts = chunk["city"].value_counts()

        for key, value in counts.items():
            stats[key] = stats.get(key, 0) + value

    print("City distribution:")
    print(stats)

    return stats


def optimise_dtypes(df):
    before = df.memory_usage(deep=True).sum() / 1024 / 1024

    for col in df.select_dtypes(include=["int64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")

    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="float")

    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype("category")

    after = df.memory_usage(deep=True).sum() / 1024 / 1024

    print(f"Memory before: {before:.2f} MB")
    print(f"Memory after: {after:.2f} MB")
    print(f"Reduced: {before - after:.2f} MB")

    return df


def run_data_loader():
    df = load_from_mongodb()

    flat_df = flatten_data_column(df)

    save_to_csv(flat_df)

    df_csv = load_csv()

    process_csv_in_chunks()
    process_chunks_per_language()

    optimised_df = optimise_dtypes(df_csv)

    return optimised_df


if __name__ == "__main__":
    run_data_loader()