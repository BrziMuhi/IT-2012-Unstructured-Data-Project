import pandas as pd
import pymysql


def get_connection(
    host="localhost",
    user="root",
    password="",
    database="tourism_db",
    port=3306
):
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset="utf8mb4"
    )


def create_places_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS place_analytics (
        place_id VARCHAR(100) PRIMARY KEY,
        source VARCHAR(100),
        timestamp_value VARCHAR(100),
        name TEXT,
        city VARCHAR(100),
        country VARCHAR(100),
        categories TEXT,
        longitude DOUBLE,
        latitude DOUBLE,
        website TEXT,
        formatted_address TEXT,
        timestamp_year INT
    )
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()


def populate_places(conn, csv_path="processed/cleaned/cleaned_data.csv"):
    df = pd.read_csv(csv_path)

    required_cols = [
        "_id", "source", "timestamp", "name", "city", "country",
        "categories", "longitude", "latitude", "website",
        "formatted_address", "timestamp_year"
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            place_id = str(row["_id"])

            if place_id == "nan" or place_id.strip() == "":
                continue

            cursor.execute(
                """
                REPLACE INTO place_analytics
                (
                    place_id, source, timestamp_value, name, city, country,
                    categories, longitude, latitude, website,
                    formatted_address, timestamp_year
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    place_id,
                    str(row["source"]),
                    str(row["timestamp"]),
                    str(row["name"]),
                    str(row["city"]),
                    str(row["country"]),
                    str(row["categories"]),
                    float(row["longitude"]) if pd.notna(row["longitude"]) else None,
                    float(row["latitude"]) if pd.notna(row["latitude"]) else None,
                    str(row["website"]),
                    str(row["formatted_address"]),
                    int(row["timestamp_year"]) if pd.notna(row["timestamp_year"]) else None,
                )
            )

    conn.commit()


def query_places(conn):
    query = """
    SELECT *
    FROM place_analytics
    WHERE place_id IS NOT NULL
    """
    return pd.read_sql(query, conn)