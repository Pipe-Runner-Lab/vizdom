import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_bar(df1, y_column_1, x_column, df2=None, y_column_2=None, color_column=None):

    if df2 is not None and y_column_2 != None:
        x_label = get_our_world_in_data_attributes[x_column]["label"]
        attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
        attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
        fig = go.Figure(data=[
          go.Bar(name=attr1_label, x=df1[x_column], y=df1[y_column_1], yaxis='y', offsetgroup=1),
          go.Bar(name=attr2_label, x=df2[x_column], y=df2[y_column_2], yaxis='y2', offsetgroup=2)
        ], )
        fig.update_xaxes(title_text=x_label)
        fig.update_layout(barmode='group', 
                          yaxis=dict(title=attr1_label),
                          yaxis2=dict(title=attr2_label, side='right',overlaying='y'),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                          ))
        return fig
    else:
      return px.bar(df1, y=x_column, x=y_column_1, color=color_column, labels={
                    x_column: get_our_world_in_data_attributes[x_column]["label"], 
                    y_column_1: get_our_world_in_data_attributes[y_column_1]["label"]})

    
    