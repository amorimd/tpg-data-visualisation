import datetime

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

import dash
from dash import Dash, dcc, callback, html, Input, Output
import dash_bootstrap_components as dbc

from data_preparation import vacation_periods_df_dict, daily_ridership_all_lines_with_line_info_pdf


####
## Page registration
####
dash.register_page(__name__, name='Ridership per line')


####
## Heading of the page
####
heading = html.H2(
    "Daily ridership per line",
    className="bg-primary text-white p-2"
)

####
## Control element: vacation period dropdown
####
vacation_dropdown = dcc.Dropdown(id='vacation_dropdown', placeholder='Select vacation period',
                                 options=[
                                        {'label': 'Autumn', 'value': 'is_autumn_vacation'},
                                        {'label': 'Winter', 'value': 'is_winter_vacation'},
                                        {'label': 'February', 'value': 'is_february_vacation'},
                                        {'label': 'Easter', 'value': 'is_easter_vacation'},
                                        {'label': 'Summer', 'value': 'is_summer_vacation'}
                                         ],
                                 multi=True, clearable=True, style={'width': '50%'})

control_panel_vacation = dbc.Card(
    dbc.CardBody(
        [html.H4("Effect of vacation periods", className="card-title"),
         html.P(
                "Select the Geneva canton vacation periods to see their effect on the ridership.",
                className="card-text",
            ),
         dbc.Row(vacation_dropdown),
        ],
        className="bg-light",
    )
)

####
## Control element: Checklist for line type
####
line_type_checklist = dcc.Checklist(
        id="line_type_checklist",
        options=[{"label": "Tramway", "value": "tramway"},
                  {"label": "Trolleybus", "value": "trolleybus"},
                  {"label": "Bus", "value": "bus"},
                  {"label": "Express", "value": "express"},
                  {"label": "School", "value": "school"},
                  {"label": "Crossborder", "value": "crossborder"}],
        value=["tramway"],
        inline=True)

control_panel_line_type = dbc.Card(
    dbc.CardBody(
        [html.H4("Line type", className="card-title"),
         html.P(
                "Select the line types to display.",
                className="card-text",
            ),
         dbc.Row(line_type_checklist),
        ],
        className="bg-light",
    )
)

####
## Create the figure
## We make a temporal view of the dataset where the ridership has been aggregated by line and date,
# and we show the total ridership per day.
# The graph has a range slider to select the period of time to show, and some buttons to quickly select some periods
# (1 month, 6 months, year to date, 1 year, all).
####

@callback(
    Output("graph_ridership_per_line", "figure"),
    Input("vacation_dropdown", "value"),
    Input("line_type_checklist", "value")
)
def daily_ridership_graph(vacation_dropdown, line_type_checklist):

    # We first filter by the line that were selected in the checklist, and then we make the graph with the filtered dataset
    mask = daily_ridership_all_lines_with_line_info_pdf.line_transport_type.isin(line_type_checklist)
    fig = px.line(daily_ridership_all_lines_with_line_info_pdf[mask],
        x="Date", y="total_number_of_boarding_passengers", color='Line',
        labels={'total_number_of_boarding_passengers': 'Number of boarding passengers'},
        )

    # Add range slider and buttons
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        )
    )

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")

    fig.update_layout(xaxis_range=[datetime.datetime(2025, 4, 30),
                            datetime.datetime(2026, 5, 1)])

    # Add a shading for the dates that are in the selected vacation periods
    if vacation_dropdown is not None:
        for vacation in vacation_dropdown:
            vacation_dates = vacation_periods_df_dict[vacation]
            for vacation_period in vacation_dates:
                fig.add_vrect(x0=vacation_period[0], x1=vacation_period[1], fillcolor="DarkOrange", opacity=0.5,
                              layer="below", line_width=0)

    return fig

######
## Graph element
######
graph = dbc.Card(
    [dcc.Graph(id="graph_ridership_per_line", style={'height': '80vh'}, mathjax=True)]
)

layout = html.Div([
        html.Div([
            html.H2('tpg ridership per line', className='text-center'),
            html.Br()
         ]),
        html.Div([
            dbc.Row([dbc.Col(control_panel_vacation), dbc.Col(control_panel_line_type)]),
            html.Br(),
            dbc.Row(graph)
        ]),
        html.Footer([
            html.Div([
                html.A('Contact: D. Amorim', href='https://github.com/amorimd'),
                html.Br(),
                html.P("Data source: tpg - transports publics genevois, en date du 29/04/2026"),
            ], className='bg-light text-dark text-center py-3 fs-6')
        ])
     ])
