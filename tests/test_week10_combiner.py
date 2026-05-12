import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.analytics.db_connector import get_connection, query_places
from src.analytics.data_combiner import compare_join_types, merge_on_place_id


MYSQL_PASSWORD = "root"


conn = get_connection(password=MYSQL_PASSWORD)
mysql_df = query_places(conn)
conn.close()

csv_df = pd.read_csv("processed/cleaned/cleaned_data.csv")

csv_df = csv_df.rename(columns={"_id": "place_id"})

metadata_df = csv_df[
    ["place_id", "name", "city", "country", "categories", "longitude", "latitude"]
].copy()

print("MySQL rows:", len(mysql_df))
print("CSV metadata rows:", len(metadata_df))

join_counts = compare_join_types(metadata_df, mysql_df)
print("\nJoin counts:")
print(join_counts)

combined_df = merge_on_place_id(metadata_df, mysql_df, how="inner")
print("\nCombined data:")
print(combined_df.head())