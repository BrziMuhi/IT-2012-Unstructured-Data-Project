from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _save(fig, output_dir, name):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / f"{name}.html", include_plotlyjs="cdn")


def interactive_category_bar(df, output_dir="outputs/visualizations/interactive"):
    data = df["categories"].value_counts().head(10).reset_index()
    data.columns = ["categories", "count"]

    fig = px.bar(
        data,
        x="count",
        y="categories",
        orientation="h",
        title="Top 10 Place Categories",
        hover_data=["categories", "count"],
    )
    _save(fig, output_dir, "interactive_category_bar")
    return fig


def interactive_city_bar(df, output_dir="outputs/visualizations/interactive"):
    data = df["city"].value_counts().head(10).reset_index()
    data.columns = ["city", "count"]

    fig = px.bar(
        data,
        x="count",
        y="city",
        orientation="h",
        title="Top Cities by Places",
        hover_data=["city", "count"],
    )
    _save(fig, output_dir, "interactive_city_bar")
    return fig


def interactive_map_scatter(df, output_dir="outputs/visualizations/interactive"):
    fig = px.scatter(
        df,
        x="longitude",
        y="latitude",
        color="categories",
        hover_data=["name", "city", "country", "categories"],
        title="Interactive Geographic Distribution of Places",
    )
    _save(fig, output_dir, "interactive_map_scatter")
    return fig


def interactive_website_pie(df, output_dir="outputs/visualizations/interactive"):
    data = df.copy()
    data["website_status"] = data["website"].apply(
        lambda x: "Has website" if x != "unknown" else "No website"
    )

    counts = data["website_status"].value_counts().reset_index()
    counts.columns = ["website_status", "count"]

    fig = px.pie(
        counts,
        names="website_status",
        values="count",
        title="Website Availability",
        hover_data=["website_status", "count"],
    )
    _save(fig, output_dir, "interactive_website_pie")
    return fig


def interactive_multi_layout(df, output_dir="outputs/visualizations/interactive"):
    category_data = df["categories"].value_counts().head(10)
    city_data = df["city"].value_counts().head(10)
    website_data = df["website"].apply(
        lambda x: "Has website" if x != "unknown" else "No website"
    ).value_counts()

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Top Categories",
            "Top Cities",
            "Coordinates",
            "Website Availability",
        ],
        specs=[
            [{"type": "bar"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "bar"}],
        ],
    )

    fig.add_trace(go.Bar(x=category_data.values, y=category_data.index, orientation="h"), row=1, col=1)
    fig.add_trace(go.Bar(x=city_data.values, y=city_data.index, orientation="h"), row=1, col=2)
    fig.add_trace(go.Scatter(x=df["longitude"], y=df["latitude"], mode="markers", text=df["name"]), row=2, col=1)
    fig.add_trace(go.Bar(x=website_data.index, y=website_data.values), row=2, col=2)

    fig.update_layout(title="Interactive Tourism Dashboard", height=800, showlegend=False)

    _save(fig, output_dir, "interactive_multi_layout")
    return fig