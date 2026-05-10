import pandas as pd


def genre_summary(df):
    return df.groupby("primary_category").agg(
        place_count=("place_id", "count"),
        avg_longitude=("longitude", "mean"),
        avg_latitude=("latitude", "mean"),
        median_year=("timestamp_year", "median")
    ).reset_index().sort_values("place_count", ascending=False)


def yearly_trends(df):
    return df.groupby("timestamp_year").agg(
        place_count=("place_id", "count"),
        unique_cities=("city", "nunique"),
        unique_categories=("primary_category", "nunique"),
        avg_latitude=("latitude", "mean")
    ).reset_index()


def top_n_per_group(df, group_col="primary_category", sort_col="latitude", n=3):
    result = (
        df.groupby(group_col, group_keys=False)
        .apply(lambda x: x.sort_values(sort_col, ascending=False).head(n))
    )

    result = result.reset_index(drop=True)

    if group_col not in result.columns:
        result[group_col] = df.loc[result.index, group_col].values

    return result