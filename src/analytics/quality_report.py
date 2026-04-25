import os
import pandas as pd
import matplotlib.pyplot as plt
from analytics.data_loader import load_csv


OUTPUT_DIR = "processed/analytics"
CHART_DIR = "processed/analytics/charts"
QUALITY_REPORT_PATH = f"{OUTPUT_DIR}/quality_report.csv"
MISSING_HEATMAP_PATH = f"{CHART_DIR}/missing_values_heatmap.png"


def missing_value_report(df):
    report = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isnull().sum().values,
        "missing_percent": (df.isnull().sum().values / len(df)) * 100
    })

    def severity(percent):
        if percent == 0:
            return "none"
        elif percent < 30:
            return "low"
        elif percent < 70:
            return "medium"
        else:
            return "high"

    report["severity"] = report["missing_percent"].apply(severity)

    print("Missing value report:")
    print(report)

    return report


def detect_zero_missing(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns
    rows = []

    for col in numeric_cols:
        zero_count = (df[col] == 0).sum()

        if zero_count > 0:
            rows.append({
                "issue_type": "zero_as_missing",
                "column": col,
                "issue_count": zero_count,
                "description": f"{zero_count} zero values found in {col}"
            })

    return pd.DataFrame(rows)


def detect_outliers_iqr(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns
    rows = []

    for col in numeric_cols:
        clean_col = df[col].dropna()

        if clean_col.empty:
            continue

        q1 = clean_col.quantile(0.25)
        q3 = clean_col.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outlier_count = ((clean_col < lower) | (clean_col > upper)).sum()

        if outlier_count > 0:
            rows.append({
                "issue_type": "outlier_iqr",
                "column": col,
                "issue_count": outlier_count,
                "description": f"{outlier_count} outliers found in {col}"
            })

    return pd.DataFrame(rows)


def validate_titles(df):
    rows = []

    if "name" in df.columns:
        missing_titles = df["name"].isnull().sum()
        empty_titles = (df["name"].fillna("").str.strip() == "").sum()

        if missing_titles > 0:
            rows.append({
                "issue_type": "missing_title",
                "column": "name",
                "issue_count": missing_titles,
                "description": "Missing values found in name column"
            })

        if empty_titles > 0:
            rows.append({
                "issue_type": "empty_title",
                "column": "name",
                "issue_count": empty_titles,
                "description": "Empty titles found in name column"
            })

    return pd.DataFrame(rows)


def detect_duplicate_ids(df):
    rows = []

    if "_id" in df.columns:
        duplicate_count = df["_id"].duplicated().sum()

        if duplicate_count > 0:
            rows.append({
                "issue_type": "duplicate_id",
                "column": "_id",
                "issue_count": duplicate_count,
                "description": "Duplicate MongoDB IDs found after flattening nested records"
            })

    return pd.DataFrame(rows)


def save_missing_heatmap(df):
    os.makedirs(CHART_DIR, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.imshow(df.isnull(), aspect="auto")
    plt.title("Missing Values Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.xticks(range(len(df.columns)), df.columns, rotation=90)
    plt.tight_layout()
    plt.savefig(MISSING_HEATMAP_PATH)
    plt.close()

    print(f"Saved missing values heatmap: {MISSING_HEATMAP_PATH}")


def run_quality_report():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = load_csv()

    missing_report = missing_value_report(df)

    missing_issues = missing_report[missing_report["missing_count"] > 0].copy()
    missing_issues["issue_type"] = "missing_values"
    missing_issues["issue_count"] = missing_issues["missing_count"]
    missing_issues["description"] = (
        missing_issues["missing_percent"].round(2).astype(str)
        + "% missing values"
    )

    missing_issues = missing_issues[
        ["issue_type", "column", "issue_count", "description", "severity"]
    ]

    zero_issues = detect_zero_missing(df)
    outlier_issues = detect_outliers_iqr(df)
    title_issues = validate_titles(df)
    duplicate_issues = detect_duplicate_ids(df)

    all_issues = pd.concat(
        [missing_issues, zero_issues, outlier_issues, title_issues, duplicate_issues],
        ignore_index=True
    )

    all_issues.to_csv(QUALITY_REPORT_PATH, index=False)

    save_missing_heatmap(df)

    print(f"Saved quality report: {QUALITY_REPORT_PATH}")
    print(all_issues)

    return all_issues


if __name__ == "__main__":
    run_quality_report()