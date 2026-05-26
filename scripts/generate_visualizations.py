import argparse
import os
import sys

sys.path.append(os.path.abspath("src"))

from visualization.chart_generator import generate_all_charts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default="processed/cleaned/cleaned_data.csv",
        help="Path to cleaned CSV file",
    )

    args = parser.parse_args()
    generate_all_charts(data_path=args.data)


if __name__ == "__main__":
    main()