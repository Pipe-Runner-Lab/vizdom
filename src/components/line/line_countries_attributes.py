import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from crawlers.url_crawlers import get_our_world_in_data_attributes

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
                  name = f"{country}, {attr1_label}"),
                  secondary_y=False)
        fig.add_trace(go.Scatter(
                  x = country_data[x_column],
                  y = country_data[y_column_2],
                  mode = 'lines',
                  opacity=0.5,
                  line={'dash': 'solid', 'color': color},
                  name = f"{country}, {attr2_label}"),
                  secondary_y=True)
    fig.update_layout(legend=dict(
                      orientation="h",
                      yanchor="bottom",
                      y=1.02,
                      xanchor="right",
                      x=1
                      ))
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return  fig