import json
from dash import html, dcc, register_page, Input, Output, callback, State, dash_table, ALL, ctx
from dash.exceptions import PreventUpdate
from components.scatter.scatter import render_scatter
from components.line.line import render_line, render_two_lines, render_country_lines
from components.bar.bar import render_bar_compare
from components.layouts.page_layouts import three_splitter_v2
from crawlers.url_crawlers import get_our_world_in_data_attributes, get_our_world_in_data_real_attributes
from data_layer.basic_data_layer import get_list_of_countries, get_total_number_of_cases_by_date, get_attribute, get_filtered_countries, create_table_bar_styles_multiple_countries, create_table_bar_styles
import dash_bootstrap_components as dbc
from utils.util import normalize
from utils.date_range import get_date_range
from utils.expression_parser import parse
from components.filter_input.filter_input import render_filter_input

# * static data

countries = get_list_of_countries()
list_of_attributes = get_our_world_in_data_attributes.items()
list_of_real_attributes = get_our_world_in_data_real_attributes.items() 
# * Register route
register_page(__name__, path="/analyse")

layout = three_splitter_v2(
    main_1=[
        html.Div(dcc.Loading(
            dcc.Graph(figure={},
                      id="analyse-main-graph-1",
                      className="main-graph",
                      style={"opacity": "0"})),
                 className="card"),
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
                value="All",
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
            html.Div([
                html.Div("Secondary Attribute", className="sub-title"),
                html.Div("Aggregation", className="sub-title"),
            ],
                className="attribute-selectors"),
            html.Div([
                dcc.Dropdown(options=[{
                    "value": attributes,
                    "label": attributes_info['label']
                } for attributes, attributes_info in list_of_real_attributes],
                    value="new_deaths",
                    id="analyse-attribute2-dropdown",
                    multi=False,
                    clearable=False
                ),
                dcc.Dropdown(options=[{
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
                className="attribute-selectors")
        ],
            className="action-wrapper"),
        html.Div([
            html.Div("Filter Panel", className="title"),
            dcc.Dropdown(options=[{
                "value":
                country,
                "label":
                countries.get(country, {}).get('label')
            } for country in countries],
                multi=True,
                placeholder="Filter by countries",
                id="analyse-country-filter",
                value=['NOR', 'IND']),
            dcc.Dropdown(options=[{
                "value": attributes,
                "label": attributes_info['label']
            } for attributes, attributes_info in list_of_real_attributes],
                multi=True,
                placeholder="Filter by attributes",
                id="analyse-attribute-filter",
                value=None),
            html.Div([],
                     className="filter-advanced-container",
                     id="analyse-filter-advanced-container"),
            html.Div([],
                     className="filter-advanced-error-container",
                     id="analyse-filter-advanced-error-container"),
            html.Div([],
                     className="filter-advanced-success-container",
                     id="analyse-filter-advanced-success-container"),
            dbc.Button(
                "Apply Filter", color="success", id="analyse-apply-filter", className='success-button'),
            dcc.Store(id='analyse-filter-data')
        ],
            id="analyse-filter-panel",
            className="action-wrapper filter-panel")
    ],
    id="analyse-page")

# ---------------------------------------------------------------------------- #
#                               FILTER CALLBACKS                               #
# ---------------------------------------------------------------------------- #


@callback(Output("analyse-filter-panel", "style"),
          Input("analyse-country-dropdown", "value"))
def toggle_filter_panel(iso_code):
    if iso_code == "All":
        return {"display": "flex"}
    else:
        return {"display": "none"}


@callback(
    Output("analyse-filter-advanced-container", "children"),
    Input("analyse-attribute-filter", "value"),
    State("analyse-filter-advanced-container", "children"),
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
    State("analyse-country-filter", "value"),
    State("analyse-attribute-filter", "value"),
    State({
        'type': 'filter-input',
        'index': ALL
    }, 'value'))
def update_filter(n_clicks, countries, attribute, filter_expressions):
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
            f"Skipping invalid filter expression for {(', ').join(error_in)}",
            color="danger",
            class_name="alert")

    if len(filter_data) > 0:
        countries = get_filtered_countries(countries, filter_data)

    success_message = "Found " + str(len(countries)) + " countries" if len(
        countries) > 0 else "No countries found, showing all countries"
    success_block = dbc.Alert(success_message,
                              color="success",
                              class_name="alert")

    return json.dumps({"countries": countries}), error_block, success_block


# ---------------------------------------------------------------------------- #
#                            BOTTOM GRAPH CALLBACKS                            #
# ---------------------------------------------------------------------------- #


@callback(Output("analyse-bottom-graph", "figure"),
          Output("analyse-bottom-graph", "style"),
          Input("analyse-country-dropdown", "value"),
          Input("analyse-bottom-graph", "relayoutData"),
          Input("analyse-filter-data", "data"))
def up_date_bottom_graph(iso_code, relayoutData, filter_data):
    start_date, end_date = get_date_range(relayoutData)

    if iso_code == "All":
        filter_data = json.loads(
            filter_data) if filter_data is not None else {}
        iso_code = filter_data.get("countries", None)

    total_num_cases = get_total_number_of_cases_by_date(
        iso_code=iso_code, start_date=start_date, end_date=end_date)
    return render_line(total_num_cases, "date", "total_cases", "location"), {"opacity": "1"}

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
    Input("analyse-aggregation1-dropdown", "value"),
    Input("analyse-aggregation2-dropdown", "value"),
    Input("analyse-bottom-graph", "relayoutData"),
    Input("analyse-filter-data", "data"),
)
def update_all_graphs(iso_code, attribute_1, attribute_2, aggregation_type_1, aggregation_type_2, relayoutData, filter_data):
    if aggregation_type_1 == 'none' and aggregation_type_2 != 'none':
        raise PreventUpdate
    elif aggregation_type_1 != 'none' and aggregation_type_2 == 'none':
        raise PreventUpdate
    
    start_date, end_date = get_date_range(relayoutData)
    column_data = None
    columns = None
    style = [{}]
    
    if iso_code == "All":
        # country filter only checked if ISO Code is All
        filter_data = json.loads(filter_data)
        iso_code = filter_data.get("countries", None)
        attribute_data_1 = get_attribute(attribute_1, start_date, end_date,
                                         iso_code, aggregation_type_1)
        attribute_data_2 = get_attribute(attribute_2, start_date, end_date,
                                         iso_code, aggregation_type_2)
        attribute_data_1[attribute_2] = attribute_data_2[attribute_2]
        
        column_data, columns, style = create_table_bar_styles_multiple_countries(
            attribute_1, attribute_2, start_date, end_date, iso_code)
        if len(iso_code) > 1:
            if aggregation_type_1 != 'none' and aggregation_type_2 != 'none':
                fig2 = render_bar_compare(attribute_data_1, attribute_1,
                                      attribute_2, "location")
                fig1 = render_scatter(attribute_data_1, attribute_1, attribute_2, 'location', aggregation_type_1, aggregation_type_2)
            else:
                attribute_date_mean_1 = get_attribute(attribute_1, start_date, end_date,
                                         iso_code, 'mean')
                attribute_date_mean_2 = get_attribute(attribute_2, start_date, end_date,
                                         iso_code, 'mean')
                attribute_date_mean_1[attribute_2] = attribute_date_mean_2[attribute_2]
                fig2 = render_country_lines(attribute_data_1,
                                        attribute_1, attribute_2, "date",
                                        "location")
                fig1 = render_scatter(attribute_date_mean_1, attribute_1, attribute_2, 'location', 'mean', 'mean')
        else:
            column_data, columns, style = create_table_bar_styles(
                        attribute_1, start_date, end_date, iso_code)
            if aggregation_type_1 == 'none' and aggregation_type_2 == 'none':
                if ((attribute_data_1[attribute_1] == attribute_data_1[attribute_1][0]).all()) or ((attribute_data_1[attribute_2] == attribute_data_1[attribute_2][0]).all()):
                    attribute_date_mean = None
                    if ((attribute_data_1[attribute_1] == attribute_data_1[attribute_1][0]).all()):
                        attribute_date_mean = get_attribute(attribute_2, start_date, end_date,
                                                iso_code, 'mean')
                        attribute_date_mean[attribute_1] = attribute_data_1[attribute_1][0]
                    
                    if ((attribute_data_1[attribute_2] == attribute_data_1[attribute_2][0]).all()):
                        attribute_date_mean = get_attribute(attribute_1, start_date, end_date,
                                            iso_code, 'mean')
                        attribute_date_mean[attribute_2] = attribute_data_1[attribute_2][0]
                
                    fig1 = render_scatter(attribute_date_mean,
                                  attribute_1, attribute_2, None, 'mean', 'mean')
                    fig2 = render_two_lines(attribute_data_1,
                                    attribute_1, attribute_2, "date")
                else:
                    attribute_data_1_norm = normalize(attribute_data_1)
                    fig1 = render_scatter(attribute_data_1_norm,
                                        attribute_1, attribute_2)
                    fig2 = render_two_lines(attribute_data_1,
                                        attribute_1, attribute_2, "date")
            else:
                fig2 = render_bar_compare(attribute_data_1, attribute_1,
                                      attribute_2, "location")
                fig1 = render_scatter(attribute_data_1, attribute_1, attribute_2, 'location', aggregation_type_1, aggregation_type_2)
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
                                  attribute_1, attribute_2, None, aggregation_type_1, aggregation_type_2)
            fig2 = render_bar_compare(attribute_data_1, attribute_1,
                                      attribute_2, "location")
        else:
            if ((attribute_data_1[attribute_1] == attribute_data_1[attribute_1][0]).all()) or ((attribute_data_1[attribute_2] == attribute_data_1[attribute_2][0]).all()):
                attribute_date_mean = None
                if ((attribute_data_1[attribute_1] == attribute_data_1[attribute_1][0]).all()):
                    attribute_date_mean = get_attribute(attribute_2, start_date, end_date,
                                                iso_code, 'mean')
                    attribute_date_mean[attribute_1] = attribute_data_1[attribute_1][0]
                    
                if ((attribute_data_1[attribute_2] == attribute_data_1[attribute_2][0]).all()):
                    attribute_date_mean = get_attribute(attribute_1, start_date, end_date,
                                            iso_code, 'mean')
                    attribute_date_mean[attribute_2] = attribute_data_1[attribute_2][0]
                
                fig1 = render_scatter(attribute_date_mean,
                                  attribute_1, attribute_2, None, 'mean', 'mean')
                fig2 = render_two_lines(attribute_data_1,
                                    attribute_1, attribute_2, "date")
            else:
                attribute_data_1_norm = normalize(attribute_data_1)
                fig1 = render_scatter(attribute_data_1_norm,
                                        attribute_1, attribute_2)
                fig2 = render_two_lines(attribute_data_1,
                                        attribute_1, attribute_2, "date")
    return fig1, fig2, {
        "opacity": "1"
    }, {
        "opacity": "1"
    }, column_data, columns, style
