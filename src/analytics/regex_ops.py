import re
from analytics.data_loader import load_csv

def extract_numbers_from_names(df):
    if "name" not in df.columns:
        return

    df["numbers_in_name"] = df["name"].str.extract(r"(\d+)")
    print("Extracted numbers from names:")
    print(df[["name", "numbers_in_name"]].head())


def filter_names_with_prefix(df, prefix="K"):
    result = df[df["name"].str.startswith(prefix, na=False)]
    print(f"Names starting with {prefix}:")
    print(result[["name"]].head())


def count_crime_words(df):
    if "categories" not in df.columns:
        return

    df["crime_count"] = df["categories"].str.count(r"crime|military|historic", flags=re.IGNORECASE)
    print("Crime-related word counts:")
    print(df[["categories", "crime_count"]].head())


def find_short_names(df):
    result = df[df["name"].str.len() < 10]
    print("Short names:")
    print(result[["name"]].head())


def extract_genres(df):
    if "categories" not in df.columns:
        return

    genres = df["categories"].str.split(", ")
    all_genres = genres.explode()

    print("Top genres:")
    print(all_genres.value_counts().head(10))


def validate_ids(df):
    valid_pattern = re.compile(r"^[a-f0-9]{24}$")

    df["valid_id"] = df["_id"].apply(lambda x: bool(valid_pattern.match(str(x))))

    print("ID validation:")
    print(df[["_id", "valid_id"]].head())


def run_regex_ops():
    df = load_csv()

    extract_numbers_from_names(df)
    filter_names_with_prefix(df)
    count_crime_words(df)
    find_short_names(df)
    extract_genres(df)
    validate_ids(df)

    print("Regex operations completed")


if __name__ == "__main__":
    run_regex_ops()