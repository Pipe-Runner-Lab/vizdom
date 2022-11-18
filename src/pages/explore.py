import plotly.express as px
from dash import html, dcc, register_page

from components.map.map import render_map
from components.line.line import render_line
from components.layouts.page_layouts import three_splitter
from data_layer.basic_data_layer import get_aggregated_total_cases_by_country

# * Register route
register_page(__name__, path="/")

data = get_aggregated_total_cases_by_country()

layout = three_splitter(
  main = dcc.Graph(
        figure=render_map(data, "total_cases")
    ),
  right = html.Div(children=[
        # html.H1(children=dcc.Graph(
        # figure=render_line(data, "date", "new_cases")
        # )),
  ]),
  bottom = html.Div(children=[]),
  id = "explore-page"
)