from dash import html, dcc, register_page, Input, Output, callback
from components.map.map import render_map
from components.scatter.scatter import render_scatter
from components.line.line import render_line
from components.line.line_compare import render_two_lines
from components.layouts.page_layouts import three_splitter
from crawlers.url_crawlers import get_our_world_in_data_attributes
from data_layer.basic_data_layer import get_aggregated_total_cases_by_country, get_list_of_countries, get_total_number_of_cases_by_date, get_attribute_by_date_range, get_attribute
import dash_bootstrap_components as dbc
from data_layer.util import resample_by

# * static data

countries = get_list_of_countries()
list_of_attributes = get_our_world_in_data_attributes.items()
# * Register route
register_page(__name__, path="/analyse")


layout = three_splitter(
    main=[
        dcc.Graph(
            figure={},
            id="analyse-main-graph-1",
            className="main-graph"
        ),
        dcc.Graph(
            figure={},
            id="analyse-main-graph-2",
            className="main-graph"
        )
    ],
    right=html.Div(children=[
        html.Div(
            [dbc.Select(
                options=[
                    {"value": "NOR", "label": "NOR"},
                    *[{"value": country, "label": country} for country in countries]
                ],
                value="NOR",
                id="analyse-country-dropdown",
                class_name="select"
            ), 
            dbc.Select(
                options=[
                    *[{"value": attributes, "label": attributes_info['label']} for attributes, attributes_info in list_of_attributes]
                ],
                value="new_cases",
                id="analyse-attribute1-dropdown",
                class_name="select"
            ), 
            dbc.Select(
                options=[
                    *[{"value": attributes, "label": attributes_info['label']} for attributes, attributes_info in list_of_attributes]
                ],
                value="new_vaccinations",
                id="analyse-attribute2-dropdown",
                class_name="select"
            )],
            className="action-wrapper"
        ),
        # html.H1(children=dcc.Graph(
        # figure=render_line(data, "date", "new_cases")
        # )),
    ]),

    bottom=dcc.Graph(
        figure={},
        id="analyse-bottom-graph",
        className="bottom-graph"
    ),
    id="analyse-page"
)


@callback(
    Output("analyse-bottom-graph", "figure"),
    Input("analyse-country-dropdown", "value"),
    Input("analyse-bottom-graph", "relayoutData")
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
    Output("analyse-main-graph-1", "figure"),
    Output("analyse-main-graph-2", "figure"),
    Input("analyse-country-dropdown", "value"),
    Input("analyse-attribute1-dropdown", "value"),
    Input("analyse-attribute2-dropdown", "value"),
    Input("analyse-bottom-graph", "relayoutData"),
)
def update_all_graphs(iso_code, attribute_1, attribute_2, relayoutData):
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    # if iso_code == "All":
    #     country_agg_data = get_aggregated_total_cases_by_country()
    # else:
    #     country_agg_data = get_aggregated_total_cases_by_country(iso_code)

    if iso_code == "All":
        attribute_data_l_1 = get_attribute_by_date_range(attribute_1, start_date, end_date)
    else:
        attribute_data_l_1 = get_attribute_by_date_range(attribute_1, start_date, end_date, iso_code)

    if iso_code == "All":
        attribute_data_l_2 = get_attribute_by_date_range(attribute_2, start_date, end_date)
    else:
        attribute_data_l_2 = get_attribute_by_date_range(attribute_2, start_date, end_date, iso_code)
    
    if iso_code == "All":
        attribute_data_s_1 = get_attribute(attribute_1)
    else:
        attribute_data_s_1 = get_attribute(attribute_1, iso_code)

    if iso_code == "All":
        attribute_data_s_2 = get_attribute(attribute_2)
    else:
        attribute_data_s_2 = get_attribute(attribute_2, iso_code)
        
    correlation = attribute_data_s_1[attribute_1].corr(attribute_data_l_2[attribute_2])
    attribute_data_s_1 = resample_by(attribute_data_s_1, 2)
    attribute_data_s_2 = resample_by(attribute_data_s_2, 2)

    return render_scatter(attribute_data_s_1, attribute_data_s_2, attribute_1, attribute_2), render_two_lines(attribute_data_l_1, attribute_data_l_2, "date", attribute_1, attribute_2)
