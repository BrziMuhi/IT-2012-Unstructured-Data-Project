from dash import html, dcc
import dash_bootstrap_components as dbc

from src.dashboard.data_access import load_movies, get_genres, get_year_range


def create_kpi_card(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title, className="text-muted"),
                html.H3(value, className="fw-bold"),
            ]
        ),
        className="shadow-sm",
    )


def create_layout():
    df = load_movies()
    genres = get_genres()
    min_year, max_year = get_year_range()

    total_movies = len(df)
    avg_rating = round(df["rating"].mean(), 2) if not df.empty else 0
    total_revenue = round(df["revenue"].sum(), 2) if not df.empty else 0
    total_budget = round(df["budget"].sum(), 2) if not df.empty else 0

    return dbc.Container(
        fluid=True,
        className="p-4 bg-dark text-light",
        children=[
            html.H1("Movie Industry Analytics Dashboard", className="text-center mb-2"),
            html.P(
                "Interactive Dash dashboard with MongoDB integration, filtering, charts, and live ticker.",
                className="text-center text-secondary mb-4",
            ),

            dbc.Row(
                [
                    dbc.Col(create_kpi_card("Total Movies", f"{total_movies:,}"), md=3),
                    dbc.Col(create_kpi_card("Average Rating", avg_rating), md=3),
                    dbc.Col(create_kpi_card("Total Revenue", f"{total_revenue:,.0f}"), md=3),
                    dbc.Col(create_kpi_card("Total Budget", f"{total_budget:,.0f}"), md=3),
                ],
                className="mb-4",
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Genre"),
                                        dcc.Dropdown(
                                            id="genre-filter",
                                            options=[{"label": g, "value": g} for g in genres],
                                            value="All",
                                            clearable=False,
                                            className="text-dark",
                                        ),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Year Range"),
                                        dcc.RangeSlider(
                                            id="year-filter",
                                            min=min_year,
                                            max=max_year,
                                            value=[min_year, max_year],
                                            marks={
                                                min_year: str(min_year),
                                                max_year: str(max_year),
                                            },
                                            tooltip={"placement": "bottom", "always_visible": False},
                                        ),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Search Movie Title"),
                                        dcc.Input(
                                            id="search-filter",
                                            type="text",
                                            placeholder="Type movie title...",
                                            debounce=True,
                                            className="form-control",
                                        ),
                                    ],
                                    md=4,
                                ),
                            ]
                        )
                    ]
                ),
                className="mb-4 bg-light text-dark",
            ),

            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="revenue-chart"), md=6),
                    dbc.Col(dcc.Graph(id="rating-chart"), md=6),
                ],
                className="mb-4",
            ),

            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="scatter-chart"), md=6),
                    dbc.Col(dcc.Graph(id="trend-chart"), md=6),
                ],
                className="mb-4",
            ),

            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="live-ticker-chart"), md=12),
                ],
                className="mb-4",
            ),

            dcc.Interval(
                id="live-interval",
                interval=3000,
                n_intervals=0,
            ),
        ],
    )