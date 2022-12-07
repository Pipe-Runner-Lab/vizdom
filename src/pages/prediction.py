import json
from dash import html, dcc, register_page, Input, Output, callback, State, ALL, ctx, no_update
from components.line.line import render_line, render_prediction_line
from components.layouts.page_layouts import three_splitter_v1
from data_layer.basic_data_layer import get_list_of_countries, get_total_number_of_cases_by_date, get_attribute
import dash_bootstrap_components as dbc
from crawlers.url_crawlers import get_our_world_in_data_real_attributes
from components.filter_input.filter_input import render_filter_input
from utils.date_range import get_date_range
from data_layer.predict import get_prediction

# * static data
countries = get_list_of_countries()
list_of_real_attributes = get_our_world_in_data_real_attributes.items()

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
                dcc.Dropdown(
                    options=[
                        *[{"value": country, "label": countries.get(country, {}).get('label')} for country in countries]
                    ],
                    value="NOR",
                    id="predict-country-dropdown",
                    multi=False,
                    clearable=False,
                ),
                html.Div(
                    "Attribute",
                    className="sub-title"
                ),
                dcc.Dropdown(
                    options=[
                        {'label': 'New Cases', 'value': 'new_cases'},
                        {'label': 'Total Cases', 'value': 'total_cases'},
                        {'label': 'New Deaths', 'value': 'new_deaths'},
                        {'label': 'Total Deaths', 'value': 'total_deaths'},
                    ],
                    # options=[{"value": attributes, "label": attributes_info['label']}
                    #          for attributes, attributes_info in list_of_real_attributes],
                    value="new_deaths",
                    id="predict-attribute-dropdown",
                    multi=False,
                    clearable=False,
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
                        {"value": "lasso", "label": "Lasso Regression"},
                        {"value": "ridge", "label": "Ridge Regression"}
                    ],
                    multi=True,
                    clearable=False,
                    placeholder="Select a model type",
                    id="predict-model-dropdown",
                    value=['lasso', 'ridge'],
                ),
                html.Div(
                    "Model Attribute Dependency",
                    className="sub-title"
                ),
                dcc.Dropdown(
                    options=[
                        {'label': 'New Cases', 'value': 'new_cases'},
                        {'label': 'Total Cases', 'value': 'total_cases'},
                        {'label': 'New Deaths', 'value': 'new_deaths'},
                        {'label': 'Total Deaths', 'value': 'total_deaths'},
                        {'label': 'People Vaccinated', 'value': 'people_vaccinated'},
                        {'label': 'People Fully Vaccinated', 'value': 'people_fully_vaccinated'},
                        {'label': 'Female Smokers', 'value': 'female_smokers'},
                        {'label': 'Male Smokers', 'value': 'male_smokers'},
                        {'label': 'Life Expectancy', 'value': 'life_expectancy'},
                        {'label': 'Cardiovasc Death Rate', 'value': 'cardiovasc_death_rate'},
                        {'label': 'Diabetes Prevalence', 'value': 'diabetes_prevalence'},
                        {'label': 'Hospital Patients', 'value': 'hosp_patients'},
                        {'label': 'Stringency Index', 'value': 'stringency_index'}
                    ], 
                    multi=True,
                    placeholder="Select attributes for model",
                    id="predict-model-attribute-dropdown",
                    value=None,
                ),
                html.Div(
                    [],
                    className="filter-advanced-success-container",
                    id="predict-filter-advanced-success-container",
                    style={"flex": "1"}
                ),
                dbc.Button(
                    "Run Prediction Model",
                    color="success",
                    id="predict-run-model",
                    className='success-button'
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
    Output("predict-model-parameter-data", "data"),
    Output("predict-filter-advanced-success-container", "children"),
    Input("predict-run-model", "n_clicks"),
    Input("predict-country-dropdown", "value"),
    Input("predict-attribute-dropdown", "value"),
    State("predict-model-dropdown", "value"),
    State("predict-model-attribute-dropdown", "value"),
    prevent_initial_call=True
)
def run_prediction(n_clicks, iso_code, target, model, attribute):
    if ctx.triggered_id == 'predict-country-dropdown' or ctx.triggered_id == 'predict-attribute-dropdown':
        return no_update, None

    success_message = "Prediction complete" if len(model) > 0 else "Please select a model type"
    success_block = dbc.Alert(
        success_message, color="success", class_name="alert")

    data = {
        "model": model,
        "attribute": attribute
    }

    return json.dumps(data), success_block

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
    return render_line(total_num_cases, "date", "total_cases_per_million", should_show_date_range=True),  {"opacity": "1"}


# ---------------------------------------------------------------------------- #
#                                DATA CALLBACKS                                #
# ---------------------------------------------------------------------------- #


@callback(
    Output("predict-main-graph-1", "figure"),
    Output("predict-main-graph-1", "style"),
    Input("predict-country-dropdown", "value"),
    Input("predict-attribute-dropdown", "value"),
    Input("predict-bottom-graph", "relayoutData"),
    Input("predict-model-parameter-data", "data"),
    prevent_initial_call=True
)
def update_all_graphs(iso_code, attribute, relayoutData, model_data_raw):
    should_predict = False
    if ctx.triggered_id == 'predict-model-parameter-data' or ctx.triggered_id == 'predict-bottom-graph':
        should_predict = True

    start_date, end_date = get_date_range(relayoutData)

    model_data = json.loads(
        model_data_raw) if model_data_raw is not None else None

    attribute_data = get_attribute(
        attribute, start_date, end_date, iso_code, None, False)

    if model_data and should_predict and len(model_data['model']) > 0:
        predictions, data_shifted = get_prediction(
            model_data['model'],
            attribute,
            iso_code,
            model_data['attribute']
        )

        fig1 = render_prediction_line(
            attribute_data, attribute, data_shifted, predictions)
    else:
        fig1 = render_prediction_line(attribute_data, attribute)

    return fig1, {"opacity": "1"}
