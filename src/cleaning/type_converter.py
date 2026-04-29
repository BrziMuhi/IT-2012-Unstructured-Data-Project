import pandas as pd

def convert_dates(df, col):
    df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def convert_numeric(df, col):
    df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def convert_category(df, col):
    df[col] = df[col].astype('category')
    return df