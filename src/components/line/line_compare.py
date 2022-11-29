import plotly.graph_objects as go
from plotly.subplots import make_subplots
from crawlers.url_crawlers import get_our_world_in_data_attributes

def render_two_lines(df1, df2, x_column, y_column_1, y_column_2, color_column=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    date_label = get_our_world_in_data_attributes[x_column]["label"]
    fig.add_trace(go.Scatter(
                  x = df1[x_column],
                  y = df1[y_column_1],
                  mode = 'lines',
                  name = attr1_label),
                  secondary_y=False)
    fig.add_trace(go.Scatter(
                  x = df2[x_column],
                  y = df2[y_column_2],
                  mode = 'lines',
                  name = attr2_label),
                  secondary_y=True)
    fig.update_layout(legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1))
    fig.update_traces(showlegend=True)
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return  fig