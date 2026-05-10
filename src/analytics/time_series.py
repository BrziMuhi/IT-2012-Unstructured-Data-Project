import pandas as pd


def parse_dates(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df


def add_date_parts(df):
    df = df.copy()
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["weekday"] = df["timestamp"].dt.day_name()
    df["quarter"] = df["timestamp"].dt.quarter
    return df


def monthly_time_series(df):
    df = df.copy()
    df = df.dropna(subset=["timestamp"])
    df = df.set_index("timestamp")

    return df.resample("ME").agg(
        place_count=("place_id", "count"),
        avg_latitude=("latitude", "mean"),
        avg_longitude=("longitude", "mean")
    ).reset_index()


def yearly_time_series(df):
    df = df.copy()
    df = df.dropna(subset=["timestamp"])
    df = df.set_index("timestamp")

    return df.resample("YE").agg(
        place_count=("place_id", "count"),
        unique_cities=("city", "nunique")
    ).reset_index()


def add_rolling_averages(monthly_df):
    monthly_df = monthly_df.copy()
    monthly_df["rolling_3"] = monthly_df["place_count"].rolling(3, min_periods=1).mean()
    monthly_df["rolling_6"] = monthly_df["place_count"].rolling(6, min_periods=1).mean()
    monthly_df["rolling_12"] = monthly_df["place_count"].rolling(12, min_periods=1).mean()
    return monthly_df