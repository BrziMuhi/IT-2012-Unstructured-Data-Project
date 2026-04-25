import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from analytics.numpy_ops import run_numpy_operations
from analytics.data_loader import run_data_loader
from analytics.data_loader import load_csv
from analytics.selector import run_selector
from analytics.regex_ops import run_regex_ops
from analytics.quality_report import run_quality_report


def test_numpy():
    result = run_numpy_operations()
    assert "ratings_mean" in result


def test_data_loader():
    df = run_data_loader()
    assert df.shape[1] >= 10  # at least 10 columns after flatten


def test_csv_loading():
    df = load_csv()
    assert not df.empty


def test_selector():
    run_selector()


def test_regex():
    run_regex_ops()


def test_quality_report():
    result = run_quality_report()
    assert not result.empty


if __name__ == "__main__":
    test_numpy()
    test_data_loader()
    test_csv_loading()
    test_selector()
    test_regex()
    test_quality_report()

    print("All Week 8 tests passed")