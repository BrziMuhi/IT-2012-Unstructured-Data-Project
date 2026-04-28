import pandas as pd
from analytics.data_loader import load_csv


def select_columns(df, columns):
    existing_columns = [col for col in columns if col in df.columns]
    result = df.loc[:, existing_columns]

    print("Selected columns:")
    print(result.head())

    return result


def filter_with_loc(df):
    if "city" not in df.columns:
        print("city column not found")
        return df

    result = df.loc[df["city"] == "Sarajevo"]

    print("Filtered with loc: city = Sarajevo")
    print(result.head())

    return result


def sample_with_iloc(df, start=0, end=5):
    result = df.iloc[start:end]

    print("Sampled rows with iloc:")
    print(result)

    return result


def filter_popular_places(df):
    if "categories" not in df.columns:
        print("categories column not found")
        return df

    result = df[
        df["categories"].str.contains("tourism", case=False, na=False)
    ]

    print("Filtered tourism places:")
    print(result.head())

    return result


def filter_with_isin(df):
    if "source" not in df.columns:
        print("source column not found")
        return df

    allowed_sources = ["geoapify_api", "geoapify_json"]

    result = df[df["source"].isin(allowed_sources)]

    print("Filtered with isin:")
    print(result.head())

    return result


def filter_with_between(df):
    if "latitude" not in df.columns:
        print("latitude column not found")
        return df

    result = df[df["latitude"].between(43.80, 43.90)]

    print("Filtered with between latitude 43.80 - 43.90:")
    print(result.head())

    return result


def run_selector():
    df = load_csv()

    select_columns(df, ["name", "city", "country", "categories"])
    filter_with_loc(df)
    sample_with_iloc(df)
    filter_popular_places(df)
    filter_with_isin(df)
    filter_with_between(df)

    print("Selector operations completed")


if __name__ == "__main__":
    run_selector()