import plotly.express as px
from dash import html, dcc, register_page, Input, Output, callback
from components.map.map import render_map
from components.line.line import render_line
from components.layouts.page_layouts import three_splitter
from data_layer.basic_data_layer import get_aggregated_total_cases_by_country, get_list_of_countries, get_total_number_of_cases_by_date
import dash_bootstrap_components as dbc

# * static data

countries = get_list_of_countries()

# * Register route
register_page(__name__, path="/")

layout = three_splitter(
    main=dcc.Graph(
        figure={},
        id="main-graph",
        className="main-graph"
    ),
    right=html.Div(children=[
        html.Div(
            dbc.Select(
                options=[
                    {"value": "All", "label": "All"},
                    *[{"value": country, "label": country} for country in countries]
                ],
                value="All",
                id="country-dropdown",
                class_name="select"
            ),
            className="action-wrapper"
        )
        # html.H1(children=dcc.Graph(
        # figure=render_line(data, "date", "new_cases")
        # )),
    ]),
    bottom=dcc.Graph(
        figure={},
        id="bottom-graph",
        className="bottom-graph"
    ),
    id="explore-page"
)


@callback(
    Output("main-graph", "figure"),
    Output("bottom-graph", "figure"),
    Input("country-dropdown", "value")
)
def on_country_change(iso_code):
    if iso_code == "All":
        country_agg_data = get_aggregated_total_cases_by_country()
    else:
        country_agg_data = get_aggregated_total_cases_by_country(iso_code)

    total_num_cases = get_total_number_of_cases_by_date()

    return render_map(country_agg_data, "total_cases"), render_line(total_num_cases, "date", "total_cases")