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
list_of_attributes = get_our_world_in_data_attributes.items()

# * Register route
register_page(__name__, path="/")

layout = three_splitter(
    main=[
        dcc.Graph(
            figure={},
            id="explore-main-graph-1",
            className="main-graph"
        ),
        dcc.Graph(
            figure={},
            id="explore-main-graph-2",
            className="main-graph"
        )
    ],
    right=[
        html.Div(
            [
                dbc.Select(
                    options=[
                        {"value": "All", "label": "All"},
                        *[{"value": country, "label": countries.get(country, {}).get('label')} for country in countries]
                    ],
                    value="All",
                    id="explore-country-dropdown",
                    class_name="select"
                ),
                dbc.Select(
                    options=[{"value": attributes, "label": attributes_info['label']}
                             for attributes, attributes_info in list_of_attributes],
                    value="new_deaths",
                    id="explore-attribute-dropdown",
                    class_name="select"
                )
            ],
            className="action-wrapper"
        ),
        html.Div(
            [
                html.Div(
                    "Country Filter",
                    className="title"
                ),
                dbc.Select(
                    options=[{"value": "mean", "label": "Mean"}, {
                        "value": "individual", "label": "Individual"}],
                    value="mean",
                    id="explore-aggregation-dropdown",
                    class_name="select"
                ),
                dcc.Dropdown(
                    options=[{"value": country, "label": countries.get(country, {}).get('label')} for country in countries],
                    multi=True,
                    id="explore-country-filter",
                    value=None
                ),
                dcc.Dropdown(
                    options=[{"value": attributes, "label": attributes_info['label']}
                             for attributes, attributes_info in list_of_attributes],
                    multi=True,
                    id="explore-attribute-filter",
                    value=None
                )
            ],
            className="action-wrapper filter-panel"
        )
    ],
    bottom=dcc.Graph(
        figure={},
        id="explore-bottom-graph",
        className="bottom-graph"
    ),
    id="explore-explore-page"
)


@callback(
    Output("explore-bottom-graph", "figure"),
    Input("explore-country-dropdown", "value"),
    Input("explore-bottom-graph", "relayoutData")
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
    Output("explore-main-graph-1", "figure"),
    Output("explore-main-graph-2", "figure"),
    Input("explore-country-dropdown", "value"),
    Input("explore-attribute-dropdown", "value"),
    Input("explore-bottom-graph", "relayoutData"),
)
def update_all_graphs(iso_code, attribute, relayoutData):
    print(iso_code)
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    if iso_code == "All":
        country_agg_data = get_aggregated_total_cases_by_country()
    else:
        country_agg_data = get_aggregated_total_cases_by_country(iso_code)

    if iso_code == "All":
        attribute_date = get_attribute(attribute, start_date, end_date)
    else:
        attribute_date = get_attribute(
            attribute, start_date, end_date, iso_code)

    return render_map(country_agg_data, "total_cases"), render_line(attribute_date, "date", attribute)
