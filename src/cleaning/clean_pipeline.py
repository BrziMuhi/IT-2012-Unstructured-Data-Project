import os
import logging
import pandas as pd
import numpy as np

from .missing_handler import (
    drop_missing_ids,
    fill_text,
    replace_zeros_with_nan,
    fill_numeric,
    drop_high_missing,
)

from .string_cleaner import clean_strings, extract_year
from .deduplicator import remove_exact_duplicates, remove_id_duplicates, count_duplicates
from .type_converter import convert_dates, convert_numeric
from .validator import validate_no_nulls


def run_cleaning_pipeline(df, output_path="processed/cleaned/cleaned_data.csv"):
    logging.info("Starting cleaning pipeline")

    df = df.copy()
    logging.info(f"Available columns: {df.columns.tolist()}")

    possible_ids = ["id", "_id", "place_id", "osm_id", "name"]
    id_col = next((col for col in possible_ids if col in df.columns), None)

    if id_col:
        df = drop_missing_ids(df, id_col)
        logging.info(f"Dropped rows with missing {id_col}")
    else:
        logging.warning("No ID column found, skipping ID missing handling")

    text_cols = [
        col for col in [
            "name", "city", "country", "website",
            "formatted_address", "address", "description",
            "title", "overview", "categories"
        ]
        if col in df.columns
    ]

    

    if text_cols:
     for col in text_cols:
        df[col] = df[col].fillna("unknown")
        df[col] = df[col].astype(str).str.strip().str.lower()        

    numeric_cols = [
        col for col in [
            "longitude", "latitude", "lon", "lat",
            "rating", "price", "rank", "distance",
            "budget", "popularity"
        ]
        if col in df.columns
    ]

    if numeric_cols:
        df = replace_zeros_with_nan(df, numeric_cols)
        df = fill_numeric(df, numeric_cols)

        for col in numeric_cols:
            df = convert_numeric(df, col)

    date_cols = [
        col for col in [
            "date", "created_at", "updated_at",
            "timestamp", "release_date"
        ]
        if col in df.columns
    ]

    for col in date_cols:
        df = convert_dates(df, col)
        df[col + "_year"] = df[col].dt.year

    df = drop_high_missing(df, threshold=0.7)

    rows_before = len(df)
    df = remove_exact_duplicates(df)
    logging.info(f"Removed exact duplicates: {rows_before - len(df)}")

    if id_col and id_col in df.columns:
        duplicate_count = count_duplicates(df, id_col)
        logging.info(f"Duplicate count in {id_col}: {duplicate_count}")
        df = remove_id_duplicates(df, id_col)

    if id_col and id_col in df.columns:
        validate_no_nulls(df, id_col)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    logging.info(f"Cleaned data saved to {output_path}")
    logging.info("Cleaning pipeline finished")

    return df