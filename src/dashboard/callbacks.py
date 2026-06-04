import random
from collections import deque

import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback

from src.dashboard.data_access import filter_movies


live_buffer = deque(maxlen=30)


def empty_figure(message):
    fig = go.Figure()
    fig.update_layout(
        title=message,
        template="plotly_dark",
        xaxis={"visible": False},
        yaxis={"visible": False},
    )
    return fig


def register_callbacks(app):
    @app.callback(
        Output("revenue-chart", "figure"),
        Input("genre-filter", "value"),
        Input("year-filter", "value"),
        Input("search-filter", "value"),
    )
    def update_revenue_chart(genre, year_range, search_text):
        df = filter_movies(genre, year_range, search_text)

        if df.empty:
            return empty_figure("No data for selected filters.")

        top_movies = df.sort_values("revenue", ascending=False).head(10)

        fig = px.bar(
            top_movies,
            x="revenue",
            y="title",
            orientation="h",
            title="Top 10 Movies by Revenue",
            labels={"revenue": "Revenue", "title": "Movie"},
            template="plotly_dark",
        )

        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        return fig

    @app.callback(
        Output("rating-chart", "figure"),
        Input("genre-filter", "value"),
        Input("year-filter", "value"),
        Input("search-filter", "value"),
    )
    def update_rating_chart(genre, year_range, search_text):
        df = filter_movies(genre, year_range, search_text)

        if df.empty:
            return empty_figure("No rating data for selected filters.")

        fig = px.histogram(
            df,
            x="rating",
            nbins=20,
            title="Rating Distribution",
            labels={"rating": "Rating"},
            template="plotly_dark",
        )

        return fig

    @app.callback(
        Output("scatter-chart", "figure"),
        Input("genre-filter", "value"),
        Input("year-filter", "value"),
        Input("search-filter", "value"),
    )
    def update_scatter_chart(genre, year_range, search_text):
        df = filter_movies(genre, year_range, search_text)

        if df.empty:
            return empty_figure("No budget/revenue data for selected filters.")

        fig = px.scatter(
            df,
            x="budget",
            y="revenue",
            hover_name="title",
            color="genre",
            title="Budget vs Revenue",
            labels={"budget": "Budget", "revenue": "Revenue"},
            template="plotly_dark",
        )

        return fig

    @app.callback(
        Output("trend-chart", "figure"),
        Input("genre-filter", "value"),
        Input("year-filter", "value"),
        Input("search-filter", "value"),
    )
    def update_trend_chart(genre, year_range, search_text):
        df = filter_movies(genre, year_range, search_text)

        if df.empty:
            return empty_figure("No yearly trend data for selected filters.")

        yearly = df.groupby("year").size().reset_index(name="movie_count")

        fig = px.line(
            yearly,
            x="year",
            y="movie_count",
            markers=True,
            title="Movies Released Per Year",
            labels={"year": "Year", "movie_count": "Number of Movies"},
            template="plotly_dark",
        )

        return fig

    @app.callback(
        Output("live-ticker-chart", "figure"),
        Input("live-interval", "n_intervals"),
    )
    def update_live_ticker(n):
        value = random.randint(50, 150)
        live_buffer.append({"tick": n, "value": value})

        ticks = [item["tick"] for item in live_buffer]
        values = [item["value"] for item in live_buffer]

        fig = px.line(
            x=ticks,
            y=values,
            markers=True,
            title="Simulated Live Movie Interest Ticker",
            labels={"x": "Tick", "y": "Interest Score"},
            template="plotly_dark",
        )

        return fig