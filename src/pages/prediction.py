import json
from dash import html, dcc, register_page, Input, Output, callback, State, ALL
from components.map.map import render_map
from components.line.line import render_line
from components.bar.bar import render_bar
from components.layouts.page_layouts import three_splitter_v1
from data_layer.basic_data_layer import get_aggregated_total_cases_by_country, get_list_of_countries, get_total_number_of_cases_by_date, get_attribute, get_filtered_countries
import dash_bootstrap_components as dbc
from crawlers.url_crawlers import get_our_world_in_data_attributes
from components.filter_input.filter_input import render_filter_input
from utils.date_range import get_date_range
from utils.expression_parser import parse

# * static data
countries = get_list_of_countries()
list_of_attributes = get_our_world_in_data_attributes.items()

# * Register route
register_page(__name__, path="/predict")

layout = three_splitter_v1(
    main=[
        html.Div(
            dcc.Loading(
                dcc.Graph(
                    figure={},
                    id="predict-main-graph-1",
                    className="main-graph",
                    style={"opacity": "0"}
                )
            ),
            className="card"
        )
    ],
    bottom=html.Div(
        dcc.Loading(
            dcc.Graph(
                figure={},
                id="predict-bottom-graph",
                className="bottom-graph",
                style={"opacity": "0"}
            ),
            id="predict-bottom-graph-loading",
            className="loading"
        ),
        className="card",
        style={"height": "100%"}
    ),
    right=[
        html.Div(
            [
                html.Div(
                    "Model Selector Panel",
                    className="title"
                ),
                html.Div(
                    "Country",
                    className="sub-title"
                ),
                dbc.Select(
                    options=[
                        *[{"value": country, "label": countries.get(country, {}).get('label')} for country in countries]
                    ],
                    value="NOR",
                    id="predict-country-dropdown",
                    class_name="select"
                ),
                html.Div(
                    "Attribute",
                    className="sub-title"
                ),
                dbc.Select(
                    options=[{"value": attributes, "label": attributes_info['label']}
                             for attributes, attributes_info in list_of_attributes],
                    value="new_deaths",
                    id="predict-attribute-dropdown",
                    class_name="select"
                )
            ],
            className="action-wrapper"
        ),
        html.Div(
            [
                html.Div(
                    "Model Parameter Panel",
                    className="title"
                ),
                html.Div(
                    "Model Type",
                    className="sub-title"
                ),
                dcc.Dropdown(
                    options=[
                        {"value": "lasso", "label": "Lasso"},
                        {"value": "ridge", "label": "Ridge"}
                    ],
                    multi=False,
                    placeholder="Select a model type",
                    id="predict-model-dropdown",
                    value=None,
                ),
                html.Div(
                    "Model Attribute Dependency",
                    className="sub-title"
                ),
                dcc.Dropdown(
                    options=[{"value": attributes, "label": attributes_info['label']}
                             for attributes, attributes_info in list_of_attributes],
                    multi=True,
                    placeholder="Select attributes for model",
                    id="predict-model-attribute-dropdown",
                    value=None,
                ),
                html.Div(
                    [],
                    className="filter-advanced-container",
                    id="predict-model-parameters-container"
                ),
                html.Div(
                    [],
                    className="filter-advanced-success-container",
                    id="predict-filter-advanced-success-container"
                ),
                dbc.Button(
                    "Run Prediction Model",
                    color="success",
                    id="predict-run-model"
                ),

                dcc.Store(id='predict-model-parameter-data')
            ],
            id="predict-filter-panel",
            className="action-wrapper filter-panel"
        )
    ],
    id="predict-page"
)


# ---------------------------------------------------------------------------- #
#                               FILTER CALLBACKS                               #
# ---------------------------------------------------------------------------- #

@ callback(
    Output("predict-model-parameters-container", "children"),
    Input("predict-model-dropdown", "value"),
    State("predict-model-parameters-container", "children"),
    prevent_initial_call=True
)
def update_model_parameter(attributes, children):
    if attributes is None:
        return []
    return [render_filter_input(attribute) for attribute in attributes]


@ callback(
    Output("predict-model-parameter-data", "data"),
    Output("predict-filter-advanced-success-container", "children"),
    Input("predict-run-model", "n_clicks"),
    State("predict-model-dropdown", "value"),
    State("predict-model-attribute-dropdown", "value"),
    State({'type': 'filter-input', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def run_prediction(n_clicks, countries, attribute, filter_expressions):
    error_in = []
    filter_data = []

    if attribute is not None:
        for attribute_command in zip(attribute, filter_expressions):
            try:
                filter_data.append(
                    (attribute_command[0], parse(attribute_command[1])))
            except Exception as e:
                error_in.append(attribute_command[0])

    if len(filter_data) > 0:
        countries = get_filtered_countries(countries, filter_data)

    success_message = "Found " + str(len(countries)) + " countries" if len(
        countries) > 0 else "No countries found, showing all countries"
    success_block = dbc.Alert(
        success_message, color="success", class_name="alert")

    return json.dumps({"countries": countries}), success_block

# ---------------------------------------------------------------------------- #
#                            BOTTOM GRAPH CALLBACKS                            #
# ---------------------------------------------------------------------------- #


@ callback(
    Output("predict-bottom-graph", "figure"),
    Output("predict-bottom-graph", "style"),
    Input("predict-country-dropdown", "value"),
    Input("predict-bottom-graph", "relayoutData")
)
def update_bottom_graph(iso_code, relayoutData):
    start_date, end_date = get_date_range(relayoutData)

    total_num_cases = get_total_number_of_cases_by_date(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    total_num_cases = total_num_cases
    return render_line(total_num_cases, "date", "total_cases"),  {"opacity": "1"}
        

# ---------------------------------------------------------------------------- #
#                                DATA CALLBACKS                                #
# ---------------------------------------------------------------------------- #


@callback(
    Output("predict-main-graph-1", "figure"),
    Output("predict-main-graph-1", "style"),
    Input("predict-country-dropdown", "value"),
    Input("predict-attribute-dropdown", "value"),
    Input("predict-bottom-graph", "relayoutData"),
    Input("predict-model-dropdown", "value"),
    Input("predict-model-attribute-dropdown", "value"),
    Input("predict-model-parameter-data", "data"),
    prevent_initial_call=True
)
def update_all_graphs(iso_code, attribute, relayoutData, model, model_attribute, parameter_data):
    start_date, end_date = get_date_range(relayoutData)

    attribute_data = get_attribute(
        attribute, start_date, end_date, iso_code)

    fig1 = render_line(
        attribute_data, "date", attribute)

    return fig1, {"opacity": "1"}
