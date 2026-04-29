def remove_exact_duplicates(df):
    return df.drop_duplicates()

def remove_id_duplicates(df, id_col):
    return df.drop_duplicates(subset=[id_col])

def count_duplicates(df, col):
    return df.duplicated(subset=[col]).sum()