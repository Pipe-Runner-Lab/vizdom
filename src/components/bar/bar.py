import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_bar(df1, x_column, y_column, color_column=None):

  
      return px.bar(df1, y=y_column, x=y_column, color=color_column, labels={
                    x_column: get_our_world_in_data_attributes[x_column]["label"], 
                    y_column: get_our_world_in_data_attributes[y_column]["label"]})
      
def render_bar_compare(df1, y_column_1, x_column, df2, y_column_2, color_column=None):
    x_label = get_our_world_in_data_attributes[x_column]["label"]
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    fig = go.Figure(data=[
                    go.Bar(name=attr1_label, x=df1[x_column], y=df1[y_column_1], yaxis='y', offsetgroup=1),
                    go.Bar(name=attr2_label, x=df2[x_column], y=df2[y_column_2], yaxis='y2', offsetgroup=2)
                    ], )
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(title_text=x_label)
    fig.update_layout(barmode='group', 
                      yaxis=dict(title=attr1_label),
                      yaxis2=dict(title=attr2_label, side='right',overlaying='y'))
    return fig

# def render_correlation(df):
#   color_1 = 'red'
#   color_2 = 'blue'
#   colors = [color_1 if (df.correlation[idx] < 0.2) and (df.correlation[idx] > -0.2) else color_2 for idx in range(len(df))]
#   fig = go.Figure(go.Bar(x=df.correlation, y=df.location, orientation='h', marker=dict(color=colors)))
#   return fig
    