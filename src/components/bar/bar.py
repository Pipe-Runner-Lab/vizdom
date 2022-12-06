import plotly.express as px
import plotly.graph_objects as go
from utils.util import truncate_df_column, truncate_string
from plotly.subplots import make_subplots
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_bar(df, x_column, y_column, color_column=None):
    fig = px.bar(df, y=y_column, x=x_column, color=color_column, labels={
                    x_column: get_our_world_in_data_attributes[x_column]["label"],
                    y_column: get_our_world_in_data_attributes[y_column]["label"]})
    return fig

def render_bar_compare(df, y_column_1, y_column_2, x_column, color_column=None):
    # x_label = get_our_world_in_data_attributes[x_column]["label"]
    x_label = x_column
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    attr1_label_truncated = truncate_string(attr1_label)
    attr2_label_truncated = truncate_string(attr2_label)
    fig = go.Figure(data=[
                    go.Bar(name=attr1_label_truncated, x=df[x_column], y=df[y_column_1], yaxis='y', offsetgroup=1),
                    go.Bar(name=attr2_label_truncated, x=df[x_column], y=df[y_column_2], yaxis='y2', offsetgroup=2)
                    ], )
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
        legend_title="",
        legend=dict(
            font=dict(
                size=12,
                color="black"
            ),
        )
    )
    fig.update_xaxes(title_text=x_label)
    fig.update_layout(barmode='group',
                      yaxis=dict(title=attr1_label),
                      yaxis2=dict(title=attr2_label, side='right',overlaying='y'))
    return fig
