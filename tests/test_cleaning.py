import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
import pytest

from src.cleaning.missing_handler import (
    report_missing,
    drop_missing_ids,
    fill_text,
    replace_zeros_with_nan,
    fill_numeric,
    drop_high_missing,
)

from src.cleaning.string_cleaner import clean_strings, extract_year
from src.cleaning.deduplicator import (
    remove_exact_duplicates,
    remove_id_duplicates,
    count_duplicates,
)

from src.cleaning.type_converter import (
    convert_dates,
    convert_numeric,
    convert_category,
)

from src.cleaning.validator import validate_no_nulls, validate_range


def test_report_missing_returns_missing_ratio():
    df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, 3]})
    report = report_missing(df)
    assert report["a"] == pytest.approx(1 / 3)
    assert report["b"] == pytest.approx(2 / 3)


def test_drop_missing_ids_removes_null_id():
    df = pd.DataFrame({"id": [1, None, 3], "title": ["a", "b", "c"]})
    cleaned = drop_missing_ids(df, "id")
    assert len(cleaned) == 2
    assert cleaned["id"].isna().sum() == 0


def test_fill_text_replaces_null_with_unknown():
    df = pd.DataFrame({"title": [None, "movie"]})
    cleaned = fill_text(df, ["title"])
    assert cleaned["title"].iloc[0] == "unknown"


def test_replace_zeros_with_nan():
    df = pd.DataFrame({"budget": [100, 0, 50]})
    cleaned = replace_zeros_with_nan(df, ["budget"])
    assert pd.isna(cleaned["budget"].iloc[1])


def test_fill_numeric_uses_median():
    df = pd.DataFrame({"budget": [100, None, 300]})
    cleaned = fill_numeric(df, ["budget"])
    assert cleaned["budget"].iloc[1] == 200


def test_drop_high_missing_removes_column():
    df = pd.DataFrame({"a": [1, None, None], "b": [1, 2, 3]})
    cleaned = drop_high_missing(df, threshold=0.5)
    assert "a" not in cleaned.columns
    assert "b" in cleaned.columns


def test_clean_strings_strips_and_lowers():
    df = pd.DataFrame({"title": ["  HELLO  ", " WORLD"]})
    cleaned = clean_strings(df, "title")
    assert cleaned["title"].iloc[0] == "hello"
    assert cleaned["title"].iloc[1] == "world"


def test_extract_year_creates_year_column():
    df = pd.DataFrame({"release_date": ["2020-05-10", "1999-01-01"]})
    cleaned = extract_year(df, "release_date")
    assert "year" in cleaned.columns
    assert cleaned["year"].iloc[0] == "2020"


def test_remove_exact_duplicates():
    df = pd.DataFrame({"id": [1, 1], "title": ["a", "a"]})
    cleaned = remove_exact_duplicates(df)
    assert len(cleaned) == 1


def test_remove_id_duplicates():
    df = pd.DataFrame({"id": [1, 1, 2], "title": ["a", "b", "c"]})
    cleaned = remove_id_duplicates(df, "id")
    assert len(cleaned) == 2


def test_count_duplicates():
    df = pd.DataFrame({"id": [1, 1, 2, 3, 3]})
    result = count_duplicates(df, "id")
    assert result == 2


def test_convert_dates_produces_datetime():
    df = pd.DataFrame({"release_date": ["2020-01-01", "bad-date"]})
    cleaned = convert_dates(df, "release_date")
    assert pd.api.types.is_datetime64_any_dtype(cleaned["release_date"])
    assert pd.isna(cleaned["release_date"].iloc[1])


def test_convert_numeric_bad_values_become_nan():
    df = pd.DataFrame({"budget": ["100", "bad", "300"]})
    cleaned = convert_numeric(df, "budget")
    assert cleaned["budget"].iloc[0] == 100
    assert pd.isna(cleaned["budget"].iloc[1])


def test_convert_category():
    df = pd.DataFrame({"language": ["en", "en", "bs"]})
    cleaned = convert_category(df, "language")
    assert str(cleaned["language"].dtype) == "category"


def test_validate_no_nulls_passes_on_clean_data():
    df = pd.DataFrame({"title": ["a", "b"]})
    validate_no_nulls(df, "title")


def test_validate_no_nulls_fails_on_null():
    df = pd.DataFrame({"title": ["a", None]})
    with pytest.raises(AssertionError):
        validate_no_nulls(df, "title")


def test_validate_range_passes():
    df = pd.DataFrame({"rating": [1, 5, 10]})
    validate_range(df, "rating", 0, 10)


def test_validate_range_fails():
    df = pd.DataFrame({"rating": [1, 15, 10]})
    with pytest.raises(AssertionError):
        validate_range(df, "rating", 0, 10)