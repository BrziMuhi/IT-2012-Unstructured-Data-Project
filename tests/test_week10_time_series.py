import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.analytics.time_series import (
    parse_dates,
    add_date_parts,
    monthly_time_series,
    yearly_time_series,
    add_rolling_averages
)

df = pd.read_csv("processed/cleaned/cleaned_data.csv")
df = df.rename(columns={"_id": "place_id"})

df = parse_dates(df)
df = add_date_parts(df)

print("DATE PARTS:")
print(df[["timestamp", "year", "month", "weekday", "quarter"]].head())

monthly = monthly_time_series(df)
yearly = yearly_time_series(df)
monthly_rolling = add_rolling_averages(monthly)

print("\nMONTHLY TIME SERIES:")
print(monthly_rolling.head())

print("\nYEARLY TIME SERIES:")
print(yearly.head())

os.makedirs("processed/analytics", exist_ok=True)
monthly_rolling.to_csv("processed/analytics/monthly_time_series.csv", index=False)
yearly.to_csv("processed/analytics/yearly_time_series.csv", index=False)