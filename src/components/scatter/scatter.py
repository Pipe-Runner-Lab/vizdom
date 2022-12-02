import plotly.express as px
import pandas as pd
from crawlers.url_crawlers import get_our_world_in_data_attributes

def render_scatter(df, x_column, y_column, color_column = None, aggregation_type_1 = " ", aggregation_type_2 = " "): 
    attr1_label = get_our_world_in_data_attributes[x_column]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column]["label"]
    fig = px.scatter(df, x_column, y_column, color_column)
    fig.update_layout(
        margin=dict(r=12, t=24, b=16)
    )

    fig.update_xaxes(title_text=f"{attr1_label} ({aggregation_type_1})")
    fig.update_yaxes(title_text=f"{attr2_label} ({aggregation_type_2})")
    return fig