import json
from dash import html, dcc, register_page, Input, Output, callback, State, ALL
from components.map.map import render_map
from components.line.line import render_line
from components.bar.bar import render_bar
from components.layouts.page_layouts import three_splitter_v1
from data_layer.basic_data_layer import get_aggregated_total_cases_by_country, get_list_of_countries, get_total_number_of_cases_by_date, get_attribute, get_filtered_countries, get_list_of_continents, get_simple_filtered_countries
import dash_bootstrap_components as dbc
from crawlers.url_crawlers import get_our_world_in_data_attributes, get_our_world_in_data_real_attributes
from components.filter_input.filter_input import render_filter_input
from utils.date_range import get_date_range
from utils.expression_parser import parse
from filters.filter_groups import custom_groups

# * static data
countries = get_list_of_countries()
continents = get_list_of_continents()
list_of_real_attributes = get_our_world_in_data_real_attributes.items()
# * Register route
register_page(__name__, path="/")

layout = three_splitter_v1(
    main=[
        html.Div(
            dcc.Loading(
                dcc.Graph(
                    figure={},
                    id="explore-main-graph-1",
                    className="main-graph",
                    style={"opacity": "0"}
                )
            ),
            className="card"
        ),
        html.Div(
            dcc.Loading(
                dcc.Graph(
                    figure={},
                    id="explore-main-graph-2",
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
                id="explore-bottom-graph",
                className="bottom-graph",
                style={"opacity": "0"}
            ),
            id="explore-bottom-graph-loading",
            className="loading"
        ),
        className="card",
        style={"height": "100%"}
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
                dcc.Dropdown(
                    options=[
                        {"value": "All", "label": "All"},
                        *[{"value": country, "label": countries.get(country, {}).get('label')} for country in countries]
                    ],
                    value="NOR",
                    id="explore-country-dropdown",
                    # class_name="select",
                    clearable=False,
                    multi=False
                ),
                html.Div(
                    [
                        html.Div(
                            "Attribute",
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
                        dcc.Dropdown(
                            options=[{"value": attributes, "label": attributes_info['label']}
                                     for attributes, attributes_info in list_of_real_attributes],
                            value="total_cases",
                            id="explore-attribute-dropdown",
                            # class_name="select",
                            clearable=False,
                            multi=False
                        ),
                        dcc.Dropdown(
                            options=[
                                {"value": "mean", "label": "Mean"},
                                {"value": "sum", "label": "Sum"},
                                {"value": "latest", "label": "Latest"},
                                {"value": "none", "label": "None"}
                            ],
                            value="none",
                            id="explore-aggregation-dropdown",
                            # class_name="select",
                            multi=False,
                            clearable=False,
                        ),
                    ],
                    className="attribute-selectors"
                ),
            ],
            className="action-wrapper"
        ),
        html.Div(
            [
                html.Div(
                    "Filter Panel",
                    className="title"
                ),
                dcc.RadioItems([
                    'Simple', 'Advanced'],
                    'Simple',
                    inline=True,
                    id="explore-filter-type-radio",
                    className="radio"
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=[{"value": continent, "label": continents.get(
                                continent, {}).get('label')} for continent in continents],
                            multi=True,
                            clearable=True,
                            placeholder="Filter by continent",
                            id="explore-continent-filter",
                            value=[]
                        ),
                        dcc.Dropdown(
                            options=[{"value": group, "label": group} for group in custom_groups.keys()],
                            multi=False,
                            clearable=True,
                            placeholder="Filter by group",
                            id="explore-group-filter",
                            value=None
                        ),
                        dcc.Dropdown(
                            options=[],
                            multi=True,
                            clearable=True,
                            placeholder="Pick groups",
                            id="explore-selected-group-filter",
                            value=[]
                        ),
                        dcc.Checklist(
                            ['Show grouped data'],
                            id="explore-should-group-checklist",
                            className="checklist",
                            value=[]
                        )
                    ],
                    id="explore-simple-filter",
                    className="inner-action-wrapper",
                    style={"display": "flex"}
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=[{"value": country, "label": countries.get(
                                country, {}).get('label')} for country in countries],
                            multi=True,
                            placeholder="Filter by countries",
                            id="explore-country-filter",
                            value=[]
                        ),
                        dcc.Dropdown(
                            options=[{"value": attributes, "label": attributes_info['label']}
                                     for attributes, attributes_info in list_of_real_attributes],
                            multi=True,
                            placeholder="Filter by attributes",
                            id="explore-attribute-filter",
                            value=[]
                        ),
                        html.Div(
                            [],
                            className="filter-advanced-container",
                            id="explore-filter-advanced-container"
                        ),
                        html.Div(
                            [],
                            className="filter-advanced-error-container",
                            id="explore-filter-advanced-error-container"
                        ),
                    ],
                    id="explore-advanced-filter",
                    className="inner-action-wrapper",
                    style={"display": "none"}
                ),
                html.Div(
                    [],
                    className="filter-advanced-success-container",
                    id="explore-filter-advanced-success-container"
                ),
                dbc.Button(
                    "Apply Filter",
                    color="success",
                    id="explore-apply-filter",
                    className='success-button'
                ),
                dcc.Store(id='explore-filter-data', data="{}")
            ],
            id="explore-filter-panel",
            className="action-wrapper filter-panel",
            style={
                "display": "none"
            }
        )
    ],
    id="explore-page"
)


# ---------------------------------------------------------------------------- #
#                               FILTER CALLBACKS                               #
# ---------------------------------------------------------------------------- #

@ callback(
    Output('explore-simple-filter', 'style'),
    Output('explore-advanced-filter', 'style'),
    Input('explore-filter-type-radio', 'value'),
    prevent_initial_call=True
)
def toggle_filter_type(filter_type):
    if filter_type == "Simple":
        return {"display": "flex"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "flex"}


@ callback(
    Output("explore-filter-panel", "style"),
    Input("explore-country-dropdown", "value")
)
def toggle_filter_panel(iso_code):
    if iso_code == "All":
        return {"display": "flex"}
    else:
        return {"display": "none"}

@ callback(
    Output("explore-selected-group-filter", "options"),
    Input("explore-group-filter", "value"),
    prevent_initial_call=True
)
def update_group_filter(selected_group):
    return [{"value": group, "label": group} for group in custom_groups.get(selected_group, {}).keys()]


@ callback(
    Output("explore-filter-advanced-container", "children"),
    Input("explore-attribute-filter", "value"),
    State("explore-filter-advanced-container", "children"),
    prevent_initial_call=True
)
def update_advanced_filter(attributes, children):
    if attributes is None:
        return []
    return [render_filter_input(attribute) for attribute in attributes]


@ callback(
    Output("explore-filter-data", "data"),
    Output("explore-filter-advanced-error-container", "children"),
    Output("explore-filter-advanced-success-container", "children"),
    Input("explore-apply-filter", "n_clicks"),
    State('explore-filter-type-radio', 'value'),
    State("explore-country-filter", "value"),
    State("explore-attribute-filter", "value"),
    State({'type': 'filter-input', 'index': ALL}, 'value'),
    State('explore-continent-filter', 'value'),
    State('explore-group-filter', 'value'),
    State('explore-selected-group-filter', 'value'),
    State('explore-should-group-checklist', 'value'),
    prevent_initial_call=True
)
def update_filter(n_clicks, filter_type, countries, attribute, filter_expressions, continents, group, selected_group, should_group):
    if filter_type == "Simple":
        if len(selected_group) == 0:
            selected_group = None

        should_group = True if len(should_group) == 1 else False

        countries, group_data = get_simple_filtered_countries(continents, group=group, selected_group=selected_group, should_group=should_group)

        success_message = "Found " + str(len(countries)) + " countries" if len(
            countries) > 0 else "No countries found, showing all countries"
        success_block = dbc.Alert(
            success_message, color="success", class_name="alert")

        return json.dumps({"countries": countries, "group": group}), [], success_block

    else:
        error_in = []
        filter_data = []
        error_block = None

        if attribute is not None:
            for attribute_command in zip(attribute, filter_expressions):
                try:
                    filter_data.append(
                        (attribute_command[0], parse(attribute_command[1])))
                except Exception as e:
                    error_in.append(attribute_command[0])

        if len(error_in) != 0:
            error_block = dbc.Alert(
                f"Skipping invalid filter expression for {(', ').join(error_in)}", color="danger", class_name="alert")

        if len(filter_data) > 0:
            countries = get_filtered_countries(countries, filter_data)

        success_message = "Found " + str(len(countries)) + " countries" if len(
            countries) > 0 else "No countries found, showing all countries"
        success_block = dbc.Alert(
            success_message, color="success", class_name="alert")

        return json.dumps({"countries": countries}), error_block, success_block

# ---------------------------------------------------------------------------- #
#                            BOTTOM GRAPH CALLBACKS                            #
# ---------------------------------------------------------------------------- #


@ callback(
    Output("explore-bottom-graph", "figure"),
    Output("explore-bottom-graph", "style"),
    Input("explore-country-dropdown", "value"),
    Input("explore-bottom-graph", "relayoutData"),
    Input("explore-filter-data", "data")
)
def update_bottom_graph(iso_code, relayoutData, filter_data):
    start_date, end_date = get_date_range(relayoutData)

    if iso_code == "All":
        filter_data = json.loads(
            filter_data) if filter_data is not None else {}
        iso_code = filter_data.get("countries", None)

    total_num_cases = get_total_number_of_cases_by_date(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    return render_line(total_num_cases, "date", "total_cases", "location", should_show_date_range=True), {"opacity": "1"}

# ---------------------------------------------------------------------------- #
#                                DATA CALLBACKS                                #
# ---------------------------------------------------------------------------- #


@callback(
    Output("explore-main-graph-1", "figure"),
    Output("explore-main-graph-2", "figure"),
    Output("explore-main-graph-1", "style"),
    Output("explore-main-graph-2", "style"),
    Input("explore-country-dropdown", "value"),
    Input("explore-attribute-dropdown", "value"),
    Input("explore-aggregation-dropdown", "value"),
    Input("explore-bottom-graph", "relayoutData"),
    Input("explore-filter-data", "data"),
    prevent_initial_call=True
)
def update_all_graphs(iso_code, attribute, aggregation_type, relayoutData, filter_data):
    start_date, end_date = get_date_range(relayoutData)

    if iso_code == "All":
        # country filter only checked if ISO Code is All
        filter_data = json.loads(
            filter_data) if filter_data is not None else {}
        iso_code = filter_data.get("countries", None)
        group = filter_data.get("group", None)

        attribute_date = get_attribute(
            attribute, start_date, end_date, iso_code, aggregation_type)
    else:
        attribute_date = get_attribute(
            attribute, start_date, end_date, iso_code, aggregation_type)

    country_agg_data = get_aggregated_total_cases_by_country(attribute, start_date, end_date, iso_code, 'mean' if aggregation_type == 'none' else aggregation_type)

    if aggregation_type != "none":
        fig2 = render_bar(attribute_date, "location", attribute)
    else:
        fig2 = render_line(attribute_date, "date", attribute, "location")

    fig1 = render_map(country_agg_data, attribute, aggregation_type = 'mean' if aggregation_type == 'none' else aggregation_type)

    return fig1, fig2, {"opacity": "1"}, {"opacity": "1"}
