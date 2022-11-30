import plotly.express as px
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_line(data, x_column, y_column, color_column=None):
    fig = px.line(
        data,
        x=x_column,
        y=y_column,
        color=color_column,
        labels={
            x_column: get_our_world_in_data_attributes[x_column]["label"],
            y_column: get_our_world_in_data_attributes[y_column]["label"],
            color_column: "" if color_column is None else get_our_world_in_data_attributes[color_column]["label"],
        }
    )
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
    )
    return fig
