import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style="whitegrid", palette="viridis")


def _save(fig, output_dir, name):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_dir / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(output_dir / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_top_categories(df, output_dir="outputs/visualizations/static"):
    data = df["categories"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    data.sort_values().plot(kind="barh", ax=ax)

    ax.set_title("Top 10 Place Categories")
    ax.set_xlabel("Number of Places")
    ax.set_ylabel("Category")

    _save(fig, output_dir, "top_10_categories")


def plot_places_per_city(df, output_dir="outputs/visualizations/static"):
    data = df["city"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    data.sort_values().plot(kind="barh", ax=ax)

    ax.set_title("Top Cities by Number of Places")
    ax.set_xlabel("Number of Places")
    ax.set_ylabel("City")

    _save(fig, output_dir, "places_per_city")


def plot_places_per_country(df, output_dir="outputs/visualizations/static"):
    data = df["country"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    data.sort_values().plot(kind="barh", ax=ax)

    ax.set_title("Top Countries by Number of Places")
    ax.set_xlabel("Number of Places")
    ax.set_ylabel("Country")

    _save(fig, output_dir, "places_per_country")


def plot_longitude_distribution(df, output_dir="outputs/visualizations/static"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["longitude"].dropna(), bins=30, ax=ax)

    ax.set_title("Longitude Distribution")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Count")

    _save(fig, output_dir, "longitude_distribution")


def plot_latitude_distribution(df, output_dir="outputs/visualizations/static"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["latitude"].dropna(), bins=30, ax=ax)

    ax.set_title("Latitude Distribution")
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Count")

    _save(fig, output_dir, "latitude_distribution")


def plot_coordinates_scatter(df, output_dir="outputs/visualizations/static"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="longitude",
        y="latitude",
        hue="categories",
        legend=False,
        ax=ax
    )

    ax.set_title("Geographic Distribution of Places")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    _save(fig, output_dir, "coordinates_scatter")


def plot_website_availability(df, output_dir="outputs/visualizations/static"):
    data = df["website"].apply(lambda x: "Has website" if x != "unknown" else "No website")
    counts = data.value_counts()

    fig, ax = plt.subplots(figsize=(8, 6))
    counts.plot(kind="bar", ax=ax)

    ax.set_title("Website Availability")
    ax.set_xlabel("Website Status")
    ax.set_ylabel("Number of Places")
    ax.tick_params(axis="x", rotation=0)

    _save(fig, output_dir, "website_availability")


def plot_dashboard_subplots(df, output_dir="outputs/visualizations/static"):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    df["categories"].value_counts().head(10).sort_values().plot(
        kind="barh",
        ax=axes[0, 0]
    )
    axes[0, 0].set_title("Top Categories")
    axes[0, 0].set_xlabel("Number of Places")

    df["city"].value_counts().head(10).sort_values().plot(
        kind="barh",
        ax=axes[0, 1]
    )
    axes[0, 1].set_title("Top Cities")
    axes[0, 1].set_xlabel("Number of Places")

    sns.scatterplot(
        data=df,
        x="longitude",
        y="latitude",
        hue="categories",
        legend=False,
        ax=axes[1, 0]
    )
    axes[1, 0].set_title("Places by Coordinates")

    website_data = df["website"].apply(lambda x: "Has website" if x != "unknown" else "No website")
    website_data.value_counts().plot(kind="bar", ax=axes[1, 1])
    axes[1, 1].set_title("Website Availability")
    axes[1, 1].tick_params(axis="x", rotation=0)

    fig.tight_layout()
    _save(fig, output_dir, "dashboard_subplots")