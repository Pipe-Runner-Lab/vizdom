import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.util import truncate_string, truncate_df_column
from datetime import timedelta, datetime
from plotly.subplots import make_subplots
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_line(data, x_column, y_column, color_column=None):
    fig = go.Figure()
    x_label = get_our_world_in_data_attributes[x_column]["label"]
    y_label = get_our_world_in_data_attributes[y_column]["label"]
    unique_countries = data.location.unique()
    for idx, country in enumerate(unique_countries):
        label_truncated = truncate_string(country)
        color = px.colors.qualitative.G10[idx % len(px.colors.qualitative.G10)]
        country_data = data[data['location'] == country]
        fig.add_trace(go.Scatter(
            x=country_data[x_column],
            y=country_data[y_column],
            mode="lines",
            line={'dash': 'solid', 'color': color},
            name=f"{label_truncated}")
            )
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
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=1)
    fig.update_xaxes(title_text=f"{x_label}")
    fig.update_yaxes(title_text=f"{y_label}")
    return fig


def render_prediction_line(data, original_col, data_shifted=None, prediction=None, delay=90):
    fig = go.Figure()
    if data_shifted is not None and prediction is not None:
        max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d %H:%M:%S') + timedelta(days=delay)
        min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d %H:%M:%S')
        data_shifted = data_shifted.loc[(data_shifted.index > min_date) & (data_shifted.index < max_date)]
        fig.add_trace(go.Scatter(
            x=data_shifted.index, y=prediction,
            line=go.scatter.Line(dash="dot", color=px.colors.qualitative.Alphabet[0]),
            name=f'Predicted {get_our_world_in_data_attributes[original_col]["label"]}',
        ))
    fig.add_trace(go.Scatter(
        x=data['date'], y=data[original_col],
        line=go.scatter.Line(dash="solid", color=px.colors.qualitative.Alphabet[1]),
        opacity=0.3 if prediction is not None else 1,
        name=f'Original {get_our_world_in_data_attributes[original_col]["label"]}',
    ))
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
        legend=dict(
            font=dict(
                size=12,
                color="black"
            ),
        )
    )
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=1)
    return fig


def render_country_lines(data, y_column_1, y_column_2, x_column, country, color_column=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    date_label = get_our_world_in_data_attributes[x_column]["label"]
    attr1_label_truncated = truncate_string(attr1_label)
    attr2_label_truncated = truncate_string(attr2_label)
    unique_countries = data.location.unique()
    for idx, country in enumerate(unique_countries):
        label_truncated = truncate_string(country)
        color = px.colors.qualitative.G10[idx % len(
            px.colors.qualitative.G10)]
        country_data = data[data['location'] == country]
        fig.add_trace(go.Scatter(
            x=country_data[x_column],
            y=country_data[y_column_1],
            legendgroup=f"group{idx}", 
            legendgrouptitle_text=f"{label_truncated}",
            mode="lines",
            line={'dash': 'solid', 'color': color},
            name=f"{attr1_label_truncated}"),
            secondary_y=False)
        fig.add_trace(go.Scatter(
            x=country_data[x_column],
            y=country_data[y_column_2],
            legendgroup=f"group{idx}",  
            legendgrouptitle_text=f"{label_truncated}",
            mode="lines",
            opacity=0.5,
            line={'dash': 'solid', 'color': color},
            name=f"{attr2_label_truncated}"),
            secondary_y=True)
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
        legend=dict(
            font=dict(
                size=10,
                color="black"
            ),
        )
    )
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=1)
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return fig


def render_two_lines(df, y_column_1, y_column_2, x_column):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    attr1_label_truncated = truncate_string(attr1_label)
    attr2_label_truncated = truncate_string(attr2_label)
    date_label = get_our_world_in_data_attributes[x_column]["label"]
    fig.add_trace(go.Scatter(
                  x=df[x_column],
                  y=df[y_column_1],
                  mode='lines',
                  name=attr1_label_truncated),
                  secondary_y=False)
    fig.add_trace(go.Scatter(
                  x=df[x_column],
                  y=df[y_column_2],
                  mode='lines',
                  name=attr2_label_truncated),
                  secondary_y=True)
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
        legend=dict(
            font=dict(
                size=12,
                color="black"
            ),
        )
    )
    fig.update_traces(showlegend=True)
    fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across", spikethickness=1)
    fig.update_yaxes(showspikes=True, spikecolor="green", spikethickness=1)
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return fig

