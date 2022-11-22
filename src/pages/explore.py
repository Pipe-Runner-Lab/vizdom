import plotly.express as px
from dash import html, dcc, register_page, Input, Output, callback
from components.map.map import render_map
from components.line.line import render_line
from components.layouts.page_layouts import three_splitter
from data_layer.basic_data_layer import get_aggregated_total_cases_by_country, get_list_of_countries, get_total_number_of_cases_by_date, get_attribute
import dash_bootstrap_components as dbc
from crawlers.url_crawlers import get_our_world_in_data_attributes

# * static data

countries = get_list_of_countries()
list_of_attributes = get_our_world_in_data_attributes.keys()

# * Register route
register_page(__name__, path="/")

layout = three_splitter(
    main=[
        dcc.Graph(
            figure={},
            id="main-graph-1",
            className="main-graph"
        ),
        dcc.Graph(
            figure={},
            id="main-graph-2",
            className="main-graph"
        )
    ],
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
        ),
        html.Div(
            dbc.Select(
                options=[
                    *[{"value": attributes, "label": attributes} for attributes in list_of_attributes]
                ],
                value="new_deaths",
                id="attribute-dropdown",
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
    Output("bottom-graph", "figure"),
    Input("country-dropdown", "value"),
    Input("bottom-graph", "relayoutData")
)
def up_date_bottom_graph(iso_code, relayoutData):
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    total_num_cases = get_total_number_of_cases_by_date(
        start_date=start_date, end_date=end_date)

    total_num_cases = total_num_cases.groupby("date").sum().reset_index()

    return render_line(total_num_cases, "date", "total_cases")


@callback(
    Output("main-graph-1", "figure"),
    Output("main-graph-2", "figure"),
    Input("country-dropdown", "value"),
    Input("attribute-dropdown", "value"),
    Input("bottom-graph", "relayoutData"),
)
def update_all_graphs(iso_code, attribute, relayoutData):
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    if iso_code == "All":
        country_agg_data = get_aggregated_total_cases_by_country()
    else:
        country_agg_data = get_aggregated_total_cases_by_country(iso_code)

    if iso_code == "All":
        attribute_date = get_attribute(attribute)
    else:
        attribute_date = get_attribute(attribute, iso_code)

    return render_map(country_agg_data, "total_cases"), render_line(attribute_date, "date", attribute)
