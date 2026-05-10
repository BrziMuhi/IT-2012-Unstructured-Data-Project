import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.analytics.pivot_builder import add_primary_category
from src.analytics.aggregator import genre_summary, yearly_trends, top_n_per_group

df = pd.read_csv("processed/cleaned/cleaned_data.csv")
df = df.rename(columns={"_id": "place_id"})
df = add_primary_category(df)

summary = genre_summary(df)
trends = yearly_trends(df)
top_places = top_n_per_group(df, group_col="primary_category", sort_col="latitude", n=3)

print("CATEGORY SUMMARY:")
print(summary.head())

print("\nYEARLY TRENDS:")
print(trends.head())

print("\nTOP 3 PLACES PER CATEGORY:")
print(top_places.head(20))

os.makedirs("processed/analytics", exist_ok=True)
summary.to_csv("processed/analytics/category_analysis.csv", index=False)
trends.to_csv("processed/analytics/yearly_trends.csv", index=False)