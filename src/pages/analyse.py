import json
from dash import html, dcc, register_page, Input, Output, callback, State, dash_table
from components.bubble.bubble import render_bubbles
from components.scatter.scatter import render_scatter
from components.line.line import render_line
from components.line.line_countries_attributes import render_country_lines
from components.bar.bar import render_bar
from components.line.line_compare import render_two_lines
from components.layouts.page_layouts import three_splitter_v2
from crawlers.url_crawlers import get_our_world_in_data_attributes
from data_layer.basic_data_layer import compute_corr_two_attributes, get_list_of_countries, get_total_number_of_cases_by_date, get_attribute
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# * static data

countries = get_list_of_countries()
list_of_attributes = get_our_world_in_data_attributes.items()
# * Register route
register_page(__name__, path="/analyse")


layout = three_splitter_v2(
    main_1=[
        dcc.Graph(
            figure={},
            id="analyse-main-graph-1",
            className="main-graph"
        ),
        html.Div(
            dash_table.DataTable(
                id='correlation-table',
                columns=[{"name": i, "id": i} for i in ['Attribute 1', 'Attribute 2', 'Correlation']],
            ),
            className="table-container"
        )
    ],
    main_2=dcc.Graph(
        figure={},
        id="analyse-main-graph-2",
        className="main-graph"
    ),
    right=[
        html.Div(
            [
                html.Div(
                    "Selector Panel",
                    className="title"
                ),
                html.Div(
                    "Country",
                    className="sub-title"
                ),
                dbc.Select(
                    options=[
                        {"value": "All", "label": "All"},
                        *[{"value": country, "label": countries.get(country, {}).get('label')} for country in countries]
                    ],
                    value="All",
                    id="analyse-country-dropdown",
                    class_name="select"
                ),
                html.Div(
                    [
                        html.Div(
                            "Primary Attribute",
                            className="sub-title"
                        ),
                        html.Div(
                            "Aggregation",
                            className="sub-title"
                        ),
                    ],
                    className="attribute-selectors"
                ),
                html.Div(
                    [
                        dbc.Select(
                            options=[{"value": attributes, "label": attributes_info['label']}
                                     for attributes, attributes_info in list_of_attributes],
                            value="new_cases",
                            id="analyse-attribute1-dropdown",
                            class_name="select"
                        ),
                        dbc.Select(
                            options=[
                                {"value": "mean", "label": "Mean"},
                                {"value": "none", "label": "None"}
                            ],
                            value="none",
                            id="analyse-aggregation-dropdown",
                            class_name="select"
                        ),
                    ],
                    className="attribute-selectors"
                ),
                html.Div(
                    [
                        html.Div(
                            "Secondary Attribute",
                            className="sub-title"
                        ),
                        html.Div(
                            "Aggregation",
                            className="sub-title"
                        ),
                    ],
                    className="attribute-selectors"
                ),
                html.Div(
                    [dbc.Select(
                        options=[{"value": attributes, "label": attributes_info['label']}
                                 for attributes, attributes_info in list_of_attributes],
                        value="new_deaths",
                        id="analyse-attribute2-dropdown",
                        class_name="select"
                    ),
                        dbc.Select(
                        options=[
                            {"value": "mean", "label": "Mean"},
                            {"value": "none", "label": "None"}
                        ],
                        value="none",
                        id="analyse-aggregation-dropdown",
                        class_name="select"
                    ), ],
                    className="attribute-selectors"
                )
            ],
            className="action-wrapper"
        ),
        html.Div(
            [
                html.Div(
                    "Filter Panel",
                    className="title"
                ),
                dcc.Dropdown(
                    options=[{"value": country, "label": countries.get(
                        country, {}).get('label')} for country in countries],
                    multi=True,
                    placeholder="Filter by countries",
                    id="analyse-country-filter",
                    value=['NOR', 'IND']
                ),
                dcc.Dropdown(
                    options=[{"value": attributes, "label": attributes_info['label']}
                             for attributes, attributes_info in list_of_attributes],
                    multi=True,
                    placeholder="Filter by attributes",
                    id="analyse-attribute-filter",
                    value=None
                ),
                dbc.Button(
                    "Apply Filter",
                    color="success",
                    id="analyse-apply-filter"
                ),

                dcc.Store(id='analyse-filter-data')
            ],
            className="action-wrapper filter-panel",
            id="analyse-filter-panel"
        )
    ],

    bottom=dcc.Graph(
        figure={},
        id="analyse-bottom-graph",
        className="bottom-graph"
    ),
    id="analyse-page"
)


@ callback(
    Output("analyse-filter-panel", "style"),
    Input("analyse-country-dropdown", "value")
)
def toggle_filter_panel(iso_code):
    if iso_code == "All":
        return {"display": "block"}
    else:
        return {"display": "none"}


@ callback(
    Output("analyse-filter-data", "data"),
    Input("analyse-apply-filter", "n_clicks"),
    State("analyse-country-filter", "value"),
)
def up_date_filter(n_clicks, countries):
    return json.dumps({
        "countries": countries
    })


@callback(
    Output("analyse-bottom-graph", "figure"),
    Input("analyse-country-dropdown", "value"),
    Input("analyse-bottom-graph", "relayoutData"),
    Input("analyse-filter-data", "data")
)
def up_date_bottom_graph(iso_code, relayoutData, filter_data):
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    if iso_code == "All":
        filter_data = json.loads(filter_data)
        iso_code = filter_data.get("countries", None)
        total_num_cases = get_total_number_of_cases_by_date(
            iso_code=iso_code, start_date=start_date, end_date=end_date)
        return render_line(total_num_cases, "date", "total_cases", "location")
    else:
        total_num_cases = get_total_number_of_cases_by_date(
            iso_code=iso_code, start_date=start_date, end_date=end_date)
        total_num_cases = total_num_cases
        return render_line(total_num_cases, "date", "total_cases")


@callback(
    Output("analyse-main-graph-1", "figure"),
    Output("analyse-main-graph-2", "figure"),
    Input("analyse-country-dropdown", "value"),
    Input("analyse-attribute1-dropdown", "value"),
    Input("analyse-attribute2-dropdown", "value"),
    Input("analyse-aggregation-dropdown", "value"),
    Input("analyse-bottom-graph", "relayoutData"),
    Input("analyse-filter-data", "data"),
)
def update_all_graphs(iso_code, attribute_1, attribute_2, aggregation_type, relayoutData, filter_data):
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    if iso_code == "All":
        # country filter only checked if ISO Code is All
        filter_data = json.loads(filter_data)
        iso_code = filter_data.get("countries", None)
        attribute_date_1 = get_attribute(
            attribute_1, start_date, end_date, iso_code, aggregation_type)
        attribute_date_2 = get_attribute(
            attribute_2, start_date, end_date, iso_code, aggregation_type)

        if aggregation_type == "mean":
            fig2 = render_bar(attribute_date_1, attribute_1,
                              "location", attribute_date_2, attribute_2)
            fig1 = go.Figure()

        else:
            attribute_date_1[attribute_2] = attribute_date_2[attribute_2]
            correlation = compute_corr_two_attributes(
                attribute_date_1, attribute_1, attribute_2)
            df = pd.DataFrame(correlation, columns=[
                              'location', 'correlation', 'attribute_1', 'attribute_2'])
            # fig1 = render_bubbles(attribute_date_1, attribute_1, attribute_2)
            fig2 = render_country_lines(
                attribute_date_1, attribute_1, attribute_2, "date", "location")
            fig1 = go.Figure()
    else:
        fig1 = None
        fig2 = None
        if aggregation_type != "mean":
            attribute_data_l_1 = get_attribute(
                attribute_1, start_date, end_date, iso_code, aggregation_type)
            attribute_data_l_2 = get_attribute(
                attribute_2, start_date, end_date, iso_code, aggregation_type)
            fig1 = render_scatter(attribute_data_l_1,
                                  attribute_data_l_2, attribute_1, attribute_2)
            fig2 = render_two_lines(
                attribute_data_l_1, attribute_data_l_2, "date", attribute_1, attribute_2)
    return fig1, fig2
