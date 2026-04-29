def validate_no_nulls(df, col):
    assert not df[col].isna().any(), f"{col} contains nulls"

def validate_range(df, col, min_val, max_val):
    assert df[col].between(min_val, max_val).all(), f"{col} out of range"