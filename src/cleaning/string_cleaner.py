def clean_strings(df, col):
    df[col] = df[col].str.strip().str.lower()
    return df

def extract_year(df, date_col):
    df['year'] = df[date_col].str.extract(r'(\d{4})')
    return df