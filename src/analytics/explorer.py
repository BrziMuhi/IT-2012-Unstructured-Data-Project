import os
import pandas as pd
import matplotlib.pyplot as plt


CHART_DIR = "processed/analytics/charts"


def inspect_dataframe(df):
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nHead:")
    print(df.head())

    print("\nInfo:")
    print(df.info())

    print("\nDescribe:")
    print(df.describe(include="all"))


def categorical_reports(df):
    for col in df.select_dtypes(include=["object", "category"]).columns:
        print(f"\nColumn: {col}")
        print("Unique values:", df[col].nunique())
        print(df[col].value_counts().head(10))


def extract_release_year(df):
    date_columns = ["release_date", "date", "published_at"]

    for col in date_columns:
        if col in df.columns:
            df["release_year"] = pd.to_datetime(df[col], errors="coerce").dt.year
            print("Created release_year from:", col)
            return df

    print("No release date column found")
    return df


def save_distribution_chart(df, column_name):
    if column_name not in df.columns:
        print(f"Column {column_name} not found")
        return

    os.makedirs(CHART_DIR, exist_ok=True)

    plt.figure(figsize=(8, 5))

    if pd.api.types.is_numeric_dtype(df[column_name]):
        df[column_name].dropna().hist()
    else:
        df[column_name].value_counts().head(10).plot(kind="bar")

    plt.title(f"Distribution of {column_name}")
    plt.xlabel(column_name)
    plt.ylabel("Count")
    plt.tight_layout()

    path = f"{CHART_DIR}/{column_name}_distribution.png"
    plt.savefig(path)
    plt.close()

    print(f"Saved chart: {path}")


def run_exploration(df):
    print("Starting EDA")

    inspect_dataframe(df)
    categorical_reports(df)
    df = extract_release_year(df)

    possible_chart_columns = [
        "vote_average",
        "rating",
        "popularity",
        "original_language",
        "language",
        "release_year",
        "categories",
        "category"
    ]

    for col in possible_chart_columns:
        if col in df.columns:
            save_distribution_chart(df, col)

    print("Finished EDA")
    return df


if __name__ == "__main__":
    from data_loader import load_csv

    df = load_csv()
    run_exploration(df)