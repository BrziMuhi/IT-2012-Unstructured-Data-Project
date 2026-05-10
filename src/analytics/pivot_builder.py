import pandas as pd


def add_primary_category(df):
    df = df.copy()
    df["primary_category"] = (
        df["categories"]
        .fillna("unknown")
        .astype(str)
        .str.split(",")
        .str[0]
        .str.strip()
    )
    return df


def wide_to_long(df):
    return pd.melt(
        df,
        id_vars=["place_id", "name", "city", "country", "primary_category"],
        value_vars=["longitude", "latitude", "timestamp_year"],
        var_name="metric",
        value_name="value"
    )


def long_to_wide(long_df):
    return long_df.pivot(
        index="place_id",
        columns="metric",
        values="value"
    ).reset_index()


def category_year_pivot(df):
    return pd.pivot_table(
        df,
        values="place_id",
        index="timestamp_year",
        columns="primary_category",
        aggfunc="count",
        fill_value=0,
        margins=True
    )


def city_category_crosstab(df):
    return pd.crosstab(
        df["city"],
        df["primary_category"],
        margins=True
    )