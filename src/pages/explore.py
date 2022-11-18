import plotly.express as px
from dash import html, dcc, register_page
from connection.db_connector import DBConnection
from components.layouts.page_layouts import three_splitter

# * Register route
register_page(__name__, path="/")

dummy_df = DBConnection().get_df('iso_code, date, new_cases', 'covid', 'iso_code = "USA"')

fig = px.line(dummy_df, x="date", y="new_cases")

layout = three_splitter(
  main = dcc.Graph(
        id='example-graph',
        figure=fig
    ),
  right = html.Div(children=[]),
  bottom = html.Div(children=[]),
  id = "explore-page"
)