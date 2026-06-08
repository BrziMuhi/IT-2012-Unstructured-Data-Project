import sys
from pathlib import Path

import dash
import dash_bootstrap_components as dbc

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from src.dashboard.layout import create_layout
from src.dashboard.callbacks import register_callbacks


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.title = "Movie Industry Analytics Dashboard"
app.layout = create_layout()

server = app.server

register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)