import plotly.express as px
import json
from dash import html, dcc, register_page, Input, Output, callback, State
from components.map.map import render_map
from components.line.line import render_line
from components.bar.bar import render_bar
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
                ),
                dbc.Select(
                    options=[
                        {"value": "mean", "label": "Mean"},
                        {"value": "individual", "label": "Individual"}
                    ],
                    value="individual",
                    id="explore-aggregation-dropdown",
                    class_name="select"
                ),
            ],
            className="action-wrapper"
        ),
        html.Div(
            [
                html.Div(
                    "Country Filter",
                    className="title"
                ),
                dbc.Alert("Filters applied only if 'All' countries are selected",
                          color="warning", class_name="alert"),
                dcc.Dropdown(
                    options=[{"value": country, "label": countries.get(
                        country, {}).get('label')} for country in countries],
                    multi=True,
                    placeholder="Filter by countries",
                    id="explore-country-filter",
                    value=['NOR', 'IND']
                ),
                dcc.Dropdown(
                    options=[{"value": attributes, "label": attributes_info['label']}
                             for attributes, attributes_info in list_of_attributes],
                    multi=True,
                    placeholder="Filter by attributes",
                    id="explore-attribute-filter",
                    value=None
                ),
                dbc.Button(
                    "Apply Filter",
                    color="success",
                    id="explore-apply-filter"
                ),

                dcc.Store(id='explore-filter-data')
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


@ callback(
    Output("explore-filter-data", "data"),
    Input("explore-apply-filter", "n_clicks"),
    State("explore-country-filter", "value"),
)
def up_date_filter(n_clicks, countries):
    return json.dumps({
        "countries": countries
    })


@ callback(
    Output("explore-bottom-graph", "figure"),
    Input("explore-country-dropdown", "value"),
    Input("explore-bottom-graph", "relayoutData"),
    Input("explore-filter-data", "data")
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
    Output("explore-main-graph-1", "figure"),
    Output("explore-main-graph-2", "figure"),
    Input("explore-country-dropdown", "value"),
    Input("explore-attribute-dropdown", "value"),
    Input("explore-aggregation-dropdown", "value"),
    Input("explore-bottom-graph", "relayoutData"),
    Input("explore-filter-data", "data"),
)
def update_all_graphs(iso_code, attribute, aggregation_type, relayoutData, filter_data):
    relayoutData = {} if relayoutData is None else relayoutData
    start_date = relayoutData.get("xaxis.range[0]", None)
    end_date = relayoutData.get("xaxis.range[1]", None)

    # aggregate type plays a role in deciding how data should be shown when multiple countries are selected

    if iso_code == "All":
        # country filter only checked if ISO Code is All
        filter_data = json.loads(filter_data)
        iso_code = filter_data.get("countries", None)
        country_agg_data = get_aggregated_total_cases_by_country(start_date, end_date, iso_code)
        attribute_date = get_attribute(attribute, start_date, end_date, iso_code, aggregation_type)

        if aggregation_type == "mean":
            fig2 = render_bar(attribute_date, "location", attribute)
        else:
            fig2 = render_line(attribute_date, "date", attribute, "location")

        fig1= render_map(country_agg_data, "total_cases")
    else:
        country_agg_data = get_aggregated_total_cases_by_country(start_date, end_date, iso_code)
        attribute_date = get_attribute(
            attribute, start_date, end_date, iso_code)
        fig1, fig2 = render_map(country_agg_data, "total_cases"), render_line(attribute_date, "date", attribute)

    return fig1, fig2