# Data visualization dashboard for the tpg data
#
# Data source: tpg - transports publics genevois, en date du 29/04/2026
# Data source: MeteoSuisse, Automatic Weather Station Geneve Cointrin GVE, en date du 29/04/2026

# This app uses Dash/Plotly to build a webpage were different visuals
# present the tpg ridership data

import numpy as np
import polars as pl
import pandas as pd

import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Ridership Data Visualization",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)


if __name__ == '__main__':
    app.run(debug=False)