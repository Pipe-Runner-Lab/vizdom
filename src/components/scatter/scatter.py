import plotly.express as px
from utils.util import truncate_df_column
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_scatter(df, y_column, x_column, size_column=None, color_column=None, aggregation_type_1=None, aggregation_type_2=None):
    # attr1_label = get_our_world_in_data_attributes[x_column]["label"]
    print(df, y_column, x_column, size_column, color_column)
    x_label = x_column
    attr2_label = get_our_world_in_data_attributes[y_column]["label"]
    if color_column:
        df = truncate_df_column(df, color_column)
    fig = px.scatter(df, x_column, y_column, color_column, size=size_column)
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
    if aggregation_type_1 == None and aggregation_type_2 == None:
        fig.update_xaxes(title_text=f"{x_label}")
        fig.update_yaxes(title_text=f"{attr2_label}")
    else:
        fig.update_xaxes(title_text=f"{x_label} ({aggregation_type_1})")
        fig.update_yaxes(title_text=f"{attr2_label} ({aggregation_type_2})")
    return fig
