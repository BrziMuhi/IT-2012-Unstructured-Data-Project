def top_categories_by_count(df, n=10):
    return (
        df.groupby("primary_category")
        .agg(place_count=("place_id", "count"))
        .reset_index()
        .sort_values("place_count", ascending=False)
        .head(n)
    )


def city_distribution(df):
    return (
        df.groupby("city")
        .agg(place_count=("place_id", "count"))
        .reset_index()
        .sort_values("place_count", ascending=False)
    )


def source_distribution(df):
    return (
        df.groupby("source")
        .agg(place_count=("place_id", "count"))
        .reset_index()
        .sort_values("place_count", ascending=False)
    )


def yearly_volume(df):
    return (
        df.groupby("timestamp_year")
        .agg(place_count=("place_id", "count"))
        .reset_index()
        .sort_values("timestamp_year")
    )


def run_all_questions(df):
    print("\nQUESTION 1: Which categories have the most places?")
    print(top_categories_by_count(df))

    print("\nQUESTION 2: Which cities have the most places?")
    print(city_distribution(df))

    print("\nQUESTION 3: Which data source contributed the most places?")
    print(source_distribution(df))

    print("\nQUESTION 4: How many places were collected per year?")
    print(yearly_volume(df))