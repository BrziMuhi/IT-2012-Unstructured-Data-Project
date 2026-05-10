import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.analytics.pivot_builder import (
    add_primary_category,
    wide_to_long,
    long_to_wide,
    category_year_pivot,
    city_category_crosstab
)

df = pd.read_csv("processed/cleaned/cleaned_data.csv")
df = df.rename(columns={"_id": "place_id"})

df = add_primary_category(df)

long_df = wide_to_long(df)
print("LONG FORMAT:")
print(long_df.head())

wide_df = long_to_wide(long_df)
print("\nWIDE FORMAT:")
print(wide_df.head())

pivot = category_year_pivot(df)
print("\nCATEGORY/YEAR PIVOT:")
print(pivot.head())

crosstab = city_category_crosstab(df)
print("\nCITY/CATEGORY CROSSTAB:")
print(crosstab.head())

os.makedirs("processed/analytics", exist_ok=True)
pivot.to_csv("processed/analytics/pivot_category_year.csv")
crosstab.to_csv("processed/analytics/city_category_crosstab.csv")