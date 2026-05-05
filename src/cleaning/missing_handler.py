import pandas as pd
import numpy as np

def report_missing(df):
    report = df.isna().mean().sort_values(ascending=False)
    return report

def drop_missing_ids(df, id_col):
    return df.dropna(subset=[id_col])

def fill_text(df, text_cols):
    for col in text_cols:
        df[col] = df[col].fillna("unknown")
    return df

def replace_zeros_with_nan(df, cols):
    for col in cols:
        df[col] = df[col].replace(0, np.nan)
    return df

def fill_numeric(df, cols):
    for col in cols:
        df[col] = df[col].fillna(df[col].median())
    return df

def drop_high_missing(df, threshold=0.5):
    missing_ratio = df.isna().mean()
    cols_to_drop = missing_ratio[missing_ratio > threshold].index
    return df.drop(columns=cols_to_drop)