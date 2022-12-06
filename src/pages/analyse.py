import json
from dash import html, dcc, register_page, Input, Output, callback, State, dash_table, ALL, ctx
from dash.exceptions import PreventUpdate
from components.scatter.scatter import render_scatter
from components.line.line import render_line, render_two_lines, render_country_lines
from components.bar.bar import render_bar_compare
from components.layouts.page_layouts import three_splitter_v2
from crawlers.url_crawlers import get_our_world_in_data_attributes, get_our_world_in_data_real_attributes
from data_layer.basic_data_layer import get_list_of_countries, get_total_number_of_cases_by_date, get_attribute, get_filtered_countries, create_table_bar_styles_multiple_countries, create_table_bar_styles, get_simple_filtered_countries, get_list_of_continents
import dash_bootstrap_components as dbc
from utils.util import normalize
from utils.date_range import get_date_range
from utils.expression_parser import parse
from components.filter_input.filter_input import render_filter_input

# * static data

countries = get_list_of_countries()
continents = get_list_of_continents()
list_of_attributes = get_our_world_in_data_attributes.items()
list_of_real_attributes = get_our_world_in_data_real_attributes.items()
# * Register route
register_page(__name__, path="/analyse")

layout = three_splitter_v2(
    main_1=[
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(
                            dcc.Graph(figure={},
                                      id="analyse-main-graph-1",
                                      className="main-graph",
                                      style={"opacity": "0"})
                        )
                    ],
                    className="card"
                ),
                html.Button(
                    html.I(className="fa-sharp fa-solid fa-exchange"),
                    id='analyse-swap-button',
                    className="swap-button",
                    n_clicks=0
                ),
                dcc.Store(id='analyse-main-graph-swap', data=False),
            ],
            className="swap-container"
        ),
        html.Div(
            dcc.Loading(dash_table.DataTable(id="correlation-table")),
            className="table-container card",
        )
    ],
    main_2=html.Div(dcc.Loading(
        dcc.Graph(figure={},
                  id="analyse-main-graph-2",
                  className="main-graph",
                  style={"opacity": "0"})),
        className="card"),
    bottom=html.Div(dcc.Loading(dcc.Graph(figure={},
                                          id="analyse-bottom-graph",
                                          className="bottom-graph",
                                          style={"opacity": "0"}),
                                id="analyse-bottom-graph-loading",
                                className="loading"),
                    className="card",
                    style={"height": "100%"}),
    right=[
        html.Div([
            html.Div("Selector Panel", className="title"),
            html.Div("Country", className="sub-title"),
            dcc.Dropdown(
                options=[
                    {
                        "value": "All",
                        "label": "All"
                    },
                    *[{
                        "value": country,
                        "label": countries.get(country, {}).get('label')
                    } for country in countries
                    ]
                ],
                value="NOR",
                id="analyse-country-dropdown",
                multi=False,
                clearable=False,
            ),
            html.Div([
                html.Div("Primary Attribute", className="sub-title"),
                html.Div("Aggregation", className="sub-title"),
            ],
                className="attribute-selectors"),
            html.Div(
                [
                    dcc.Dropdown(
                        options=[
                            {
                                "value": attributes,
                                "label": attributes_info['label']
                            } for attributes, attributes_info in list_of_real_attributes
                        ],
                        value="new_cases",
                        id="analyse-attribute1-dropdown",
                        multi=False,
                        clearable=False
                    ),
                    dcc.Dropdown(
                        options=[{
                            "value": "mean",
                            "label": "Mean"
                        },
                            {
                            "value": "sum",
                            "label": "Sum"
                        },
                            {
                            "value": "latest",
                            "label": "Latest"
                        },
                            {
                            "value": "none",
                            "label": "None"
                        }
                        ],
                        value="none",
                        id="analyse-aggregation1-dropdown",
                        multi=False,
                        clearable=False
                    ),
                ],
                className="attribute-selectors"),
            html.Div(
                [
                    html.Div("Secondary Attribute", className="sub-title"),
                    html.Div("Aggregation", className="sub-title"),
                ],
                className="attribute-selectors"
            ),
            html.Div(
                [
                    dcc.Dropdown(options=[{
                        "value": attributes,
                        "label": attributes_info['label']
                    } for attributes, attributes_info in list_of_real_attributes],
                        value="new_deaths",
                        id="analyse-attribute2-dropdown",
                        multi=False,
                        clearable=False
                    ),
                    dcc.Dropdown(
                        options=[{
                            "value": "mean",
                            "label": "Mean"
                        }, {
                            "value": "sum",
                            "label": "Sum"
                        }, {
                            "value": "latest",
                            "label": "Latest"
                        }, {
                            "value": "none",
                            "label": "None"
                        }],
                        value="none",
                        id="analyse-aggregation2-dropdown",
                        multi=False,
                        clearable=False
                    ),
                ],
                className="attribute-selectors"
            ),

            html.Div(
                [
                    html.Div("Tertiary Attribute", className="sub-title"),
                    html.Div("Aggregation", className="sub-title"),
                ],
                className="attribute-selectors"
            ),
            html.Div(
                [
                    dcc.Dropdown(options=[{
                        "value": attributes,
                        "label": attributes_info['label']
                    } for attributes, attributes_info in list_of_real_attributes],
                        id="analyse-attribute3-dropdown",
                        multi=False,
                        clearable=True
                    ),
                    dcc.Dropdown(
                        options=[{
                            "value": "mean",
                            "label": "Mean"
                        }, {
                            "value": "sum",
                            "label": "Sum"
                        }, {
                            "value": "latest",
                            "label": "Latest"
                        }],
                        value="mean",
                        id="analyse-aggregation3-dropdown",
                        multi=False,
                        clearable=False
                    ),
                ],
                className="attribute-selectors"
            )
        ],
            className="action-wrapper"),
        html.Div(
            [
                html.Div("Filter Panel", className="title"),
                dcc.RadioItems([
                    'Simple', 'Advanced'],
                    'Simple',
                    inline=True,
                    id="analyse-filter-type-radio",
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
                            id="analyse-continent-filter",
                            value=[]
                        ),
                        dcc.Dropdown(
                            options=[{"value": country, "label": countries.get(
                                country, {}).get('label')} for country in countries],
                            multi=False,
                            clearable=True,
                            placeholder="Filter by group",
                            id="analyse-group-filter",
                            value=None
                        ),
                        dcc.Dropdown(
                            options=[{"value": country, "label": countries.get(
                                country, {}).get('label')} for country in countries],
                            multi=True,
                            clearable=True,
                            placeholder="Pick groups",
                            id="analyse-selected-group-filter",
                            value=[]
                        ),
                        dcc.Checklist(
                            ['Show grouped data'],
                            id="analyse-should-group-checklist",
                            className="checklist",
                            value=[]
                        )
                    ],
                    id="analyse-simple-filter",
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
                            id="analyse-country-filter",
                            value=[]
                        ),
                        dcc.Dropdown(
                            options=[{"value": attributes, "label": attributes_info['label']}
                                     for attributes, attributes_info in list_of_real_attributes],
                            multi=True,
                            placeholder="Filter by attributes",
                            id="analyse-attribute-filter",
                            value=[]
                        ),
                        html.Div(
                            [],
                            className="filter-advanced-container",
                            id="analyse-filter-advanced-container"
                        ),
                        html.Div(
                            [],
                            className="filter-advanced-error-container",
                            id="analyse-filter-advanced-error-container"
                        ),
                    ],
                    id="analyse-advanced-filter",
                    className="inner-action-wrapper",
                    style={"display": "none"}
                ),
                html.Div(
                    [],
                    className="filter-advanced-success-container",
                    id="analyse-filter-advanced-success-container"
                ),
                dbc.Button(
                    "Apply Filter", color="success", id="analyse-apply-filter", className='success-button'),
                dcc.Store(id='analyse-filter-data', data="{}"),
            ],
            id="analyse-filter-panel",
            className="action-wrapper filter-panel",
            style={
                "display": "none"
            }
        )
    ],
    id="analyse-page")

# ---------------------------------------------------------------------------- #
#                               FILTER CALLBACKS                               #
# ---------------------------------------------------------------------------- #


@ callback(
    Output('analyse-simple-filter', 'style'),
    Output('analyse-advanced-filter', 'style'),
    Input('analyse-filter-type-radio', 'value'),
    prevent_initial_call=True
)
def toggle_filter_type(filter_type):
    if filter_type == "Simple":
        return {"display": "flex"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "flex"}


@callback(
    Output("analyse-main-graph-swap", "data"),
    Input("analyse-main-graph-swap", "data"),
    Input("analyse-swap-button", "n_clicks"),
    prevent_initial_call=True
)
def toggle_main_graph(data, n_clicks):
    if ctx.triggered_id == 'analyse-swap-button':
        return not data
    else:
        raise PreventUpdate


@callback(
    Output("analyse-filter-panel", "style"),
    Input("analyse-country-dropdown", "value")
)
def toggle_filter_panel(iso_code):
    if iso_code == "All":
        return {"display": "flex"}
    else:
        return {"display": "none"}


@callback(
    Output("analyse-filter-advanced-container", "children"),
    Input("analyse-attribute-filter", "value"),
    State("analyse-filter-advanced-container", "children"),
    prevent_initial_call=True
)
def update_advanced_filter(attributes, children):
    if attributes is None:
        return []
    return [render_filter_input(attribute) for attribute in attributes]


@callback(
    Output("analyse-filter-data", "data"),
    Output("analyse-filter-advanced-error-container", "children"),
    Output("analyse-filter-advanced-success-container", "children"),
    Input("analyse-apply-filter", "n_clicks"),
    State('analyse-filter-type-radio', 'value'),
    State("analyse-country-filter", "value"),
    State("analyse-attribute-filter", "value"),
    State({'type': 'filter-input', 'index': ALL}, 'value'),
    State('analyse-continent-filter', 'value'),
    State('analyse-group-filter', 'value'),
    State('analyse-selected-group-filter', 'value'),
    State('analyse-should-group-checklist', 'value'),
    prevent_initial_call=True
)
def update_filter(n_clicks, filter_type, countries, attribute, filter_expressions, continents, group, selected_group, should_group):
    if filter_type == "Simple":
        if len(selected_group) == 0:
            selected_group = None

        should_group = True if len(should_group) == 1 else False

        countries, group = get_simple_filtered_countries(
            continents, should_group=should_group)

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


@callback(Output("analyse-bottom-graph", "figure"),
          Output("analyse-bottom-graph", "style"),
          Input("analyse-country-dropdown", "value"),
          Input("analyse-bottom-graph", "relayoutData"),
          Input("analyse-filter-data", "data"))
def update_bottom_graph(iso_code, relayoutData, filter_data):
    start_date, end_date = get_date_range(relayoutData)

    if iso_code == "All":
        filter_data = json.loads(
            filter_data) if filter_data is not None else {}
        iso_code = filter_data.get("countries", None)

    total_num_cases = get_total_number_of_cases_by_date(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    return render_line(total_num_cases, "date", "total_cases", "location", should_show_date_range=True), {"opacity": "1"}

# --------------------------- AGGREGATION ENFORCER --------------------------- #


@callback(
    Output("analyse-aggregation1-dropdown", "value"),
    Output("analyse-aggregation2-dropdown", "value"),
    Input("analyse-aggregation1-dropdown", "value"),
    Input("analyse-aggregation2-dropdown", "value"),
)
def aggregation_logic_enforcer(aggregation_type_1, aggregation_type_2):
    if ctx.triggered_id == 'analyse-aggregation1-dropdown':
        if aggregation_type_1 != 'none' and aggregation_type_2 == 'none':
            # enforce aggregation 2 to mean
            return aggregation_type_1, 'mean'

        if aggregation_type_1 == 'none' and aggregation_type_2 != 'none':
            # enforce aggregation 2 to none
            return aggregation_type_1, 'none'
    else:
        if aggregation_type_1 == 'none' and aggregation_type_2 != 'none':
            # enforce aggregation 1 to mean
            return 'mean', aggregation_type_2

        if aggregation_type_1 != 'none' and aggregation_type_2 == 'none':
            # enforce aggregation 1 to none
            return 'none', aggregation_type_2

    raise PreventUpdate


@callback(
    Output("analyse-main-graph-1", "figure"),
    Output("analyse-main-graph-2", "figure"),
    Output("analyse-main-graph-1", "style"),
    Output("analyse-main-graph-2", "style"),
    [
        Output("correlation-table", 'data'),
        Output("correlation-table", 'columns'),
        Output("correlation-table", 'style_data_conditional')
    ],
    Input("analyse-country-dropdown", "value"),
    Input("analyse-attribute1-dropdown", "value"),
    Input("analyse-attribute2-dropdown", "value"),
    Input("analyse-attribute3-dropdown", "value"),
    Input("analyse-aggregation1-dropdown", "value"),
    Input("analyse-aggregation2-dropdown", "value"),
    Input("analyse-aggregation3-dropdown", "value"),
    Input("analyse-bottom-graph", "relayoutData"),
    Input("analyse-filter-data", "data"),
    Input("analyse-main-graph-swap", "data")
)
def update_all_graphs(
    iso_code, attribute_1, attribute_2, attribute_3, aggregation_type_1, aggregation_type_2, aggregation_type_3, relayoutData, filter_data, should_swap
):
    if aggregation_type_1 == 'none' and aggregation_type_2 != 'none':
        raise PreventUpdate
    elif aggregation_type_1 != 'none' and aggregation_type_2 == 'none':
        raise PreventUpdate

    start_date, end_date = get_date_range(relayoutData)
    column_data = None
    columns = None
    style = [{}]

    filter_data = json.loads(filter_data) if filter_data is not None else {}
    iso_code_filter = filter_data.get("countries", None)

    is_single_country = iso_code != "All" or (iso_code == "All" and iso_code_filter and len(iso_code_filter) == 1)

    if not is_single_country:  
        iso_code = iso_code_filter
        group_data = filter_data.get("group", None)
        should_group = group_data
        color_label = list(group_data.keys())[0] if should_group else 'location'

        aggregation_type_1_modified = aggregation_type_1 if aggregation_type_1 != 'none' else 'mean'
        aggregation_type_2_modified = aggregation_type_2 if aggregation_type_2 != 'none' else 'mean'
        should_aggregate = (aggregation_type_1 != 'none' or aggregation_type_2 != 'none')
        
        # Fetch
        attribute_date_1 = get_attribute(attribute_1, start_date, end_date,
                                         iso_code, aggregation_type_1_modified, group=group_data)
        attribute_date_2 = get_attribute(attribute_2, start_date, end_date,
                                         iso_code, aggregation_type_2_modified, group=group_data)
        attribute_date_1[attribute_2] = attribute_date_2[attribute_2]

        if attribute_3 is not None:
            attribute_date_3 = get_attribute(attribute_3, start_date, end_date,
                                             iso_code, aggregation_type_3)
            attribute_date_1[attribute_3] = attribute_date_3[attribute_3]

        column_data, columns, style = create_table_bar_styles_multiple_countries(
            attribute_1, attribute_2, start_date, end_date, iso_code)
        
        # plotting
        fig1 = render_scatter(attribute_date_1, attribute_1, attribute_2, attribute_3, color_label, aggregation_type_1, aggregation_type_2)

        if should_aggregate or should_group:
            fig2 = render_bar_compare(attribute_date_1, attribute_1,
                                      attribute_2, color_label)
        else:
            attribute_date_1 = get_attribute(attribute_1, start_date, end_date,
                                        iso_code)
            attribute_date_2 = get_attribute(attribute_2, start_date, end_date,
                                        iso_code)
            attribute_date_1[attribute_2] = attribute_date_2[attribute_2]
            fig2 = render_country_lines(attribute_date_1, attribute_1, attribute_2, "date", 'location')
    else:
        attribute_data_1 = get_attribute(attribute_1, start_date, end_date,
                                         iso_code, aggregation_type_1)
        attribute_data_2 = get_attribute(attribute_2, start_date, end_date,
                                         iso_code, aggregation_type_2)
        attribute_data_1[attribute_2] = attribute_data_2[attribute_2]
        column_data, columns, style = create_table_bar_styles(
            attribute_1, start_date, end_date, iso_code)
        if aggregation_type_1 != 'none' and aggregation_type_2 != 'none':
            fig1 = render_scatter(attribute_data_1,
                                  attribute_1, attribute_2, None, None, aggregation_type_1, aggregation_type_2)
            fig2 = render_bar_compare(attribute_data_1, attribute_1,
                                      attribute_2, "location")
        else:
            attribute_data_1_norm = normalize(attribute_data_1)
            fig1 = render_scatter(attribute_data_1_norm,
                                  attribute_1, attribute_2)
            fig2 = render_two_lines(attribute_data_1,
                                    attribute_1, attribute_2, "date")

    if should_swap:
        fig1, fig2 = fig2, fig1

    return fig1, fig2, {
        "opacity": "1"
    }, {
        "opacity": "1"
    }, column_data, columns, style
