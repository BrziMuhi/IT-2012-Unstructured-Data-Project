import pandas as pd

from visualization.static_charts import (
    plot_top_categories,
    plot_places_per_city,
    plot_places_per_country,
    plot_longitude_distribution,
    plot_latitude_distribution,
    plot_coordinates_scatter,
    plot_website_availability,
    plot_dashboard_subplots,
)

from visualization.interactive_charts import (
    interactive_category_bar,
    interactive_city_bar,
    interactive_map_scatter,
    interactive_website_pie,
    interactive_multi_layout,
)


def generate_all_charts(
    data_path="processed/cleaned/cleaned_data.csv",
    static_dir="outputs/visualizations/static",
    interactive_dir="outputs/visualizations/interactive",
):
    df = pd.read_csv(data_path)

    static_functions = [
        plot_top_categories,
        plot_places_per_city,
        plot_places_per_country,
        plot_longitude_distribution,
        plot_latitude_distribution,
        plot_coordinates_scatter,
        plot_website_availability,
        plot_dashboard_subplots,
    ]

    interactive_functions = [
        interactive_category_bar,
        interactive_city_bar,
        interactive_map_scatter,
        interactive_website_pie,
        interactive_multi_layout,
    ]

    print("Generating static charts...")
    for func in static_functions:
        print(f"Running {func.__name__}")
        func(df, static_dir)

    print("Generating interactive charts...")
    for func in interactive_functions:
        print(f"Running {func.__name__}")
        func(df, interactive_dir)

    print("All charts generated successfully.")