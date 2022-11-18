import plotly.express as px


def render_line(data, x_column, y_column, color_column=None):
  return  px.line(data, x=x_column, y=y_column)