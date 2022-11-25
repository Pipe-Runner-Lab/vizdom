import plotly.express as px
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_bar(data, x_column, y_column, color_column=None):
    return px.bar(data, x=x_column, y=y_column, color=color_column, labels={
      x_column: get_our_world_in_data_attributes[x_column]["label"], 
      y_column: get_our_world_in_data_attributes[y_column]["label"]})
