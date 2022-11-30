import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    


def render_country_lines(data, y_column_1, y_column_2, x_column, country, color_column=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    date_label = get_our_world_in_data_attributes[x_column]["label"]
    countries = data.groupby('location').first()
    
    for idx, country in enumerate(countries.index):  
        color = px.colors.qualitative.Alphabet[idx % len(px.colors.qualitative.Alphabet)]
        country_data = data[data['location'] == country]
        fig.add_trace(go.Scatter(
                  x = country_data[x_column],
                  y = country_data[y_column_1],
                  mode = 'lines',
                  line={'dash': 'solid', 'color': color},
                  name = f"{country}, <br>{attr1_label}"),
                  secondary_y=False)
        fig.add_trace(go.Scatter(
                  x = country_data[x_column],
                  y = country_data[y_column_2],
                  mode = 'lines',
                  opacity=0.5,
                  line={'dash': 'solid', 'color': color},
                  name = f"{country}, <br>{attr2_label}"),
                  secondary_y=True)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return  fig
  
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
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.update_traces(showlegend=True)
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return  fig
