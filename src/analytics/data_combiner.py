import pandas as pd


def merge_on_place_id(left_df, right_df, how="inner"):
    return pd.merge(
        left_df,
        right_df,
        on="place_id",
        how=how,
        suffixes=("_left", "_right")
    )


def compare_join_types(left_df, right_df):
    results = {}

    for join_type in ["inner", "left", "right", "outer"]:
        merged = merge_on_place_id(left_df, right_df, how=join_type)
        results[join_type] = len(merged)

    return pd.DataFrame(
        list(results.items()),
        columns=["join_type", "row_count"]
    )


def concat_same_structure(dfs):
    return pd.concat(dfs, ignore_index=True)