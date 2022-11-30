import plotly.graph_objects as go 
from crawlers.url_crawlers import get_our_world_in_data_attributes

def render_scatter(df1, df2, x_column, y_column): 
    attr1_label = get_our_world_in_data_attributes[x_column]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column]["label"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                  x = df1[x_column],
                  y = df2[y_column],
                  mode = 'markers', 
                 ))
    fig.update_layout(legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                      ))
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
    )
    fig.update_xaxes(title_text=attr1_label)
    fig.update_yaxes(title_text=attr2_label)
    return fig