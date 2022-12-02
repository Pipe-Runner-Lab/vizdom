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


def render_prediction_line(data, original_col, data_shifted=None, prediction=None):
    fig = go.Figure()
    if data_shifted is not None and prediction is not None:
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
    )
    return fig


def render_country_lines(data, countries,  y_column_1, y_column_2, x_column, country, color_column=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    date_label = get_our_world_in_data_attributes[x_column]["label"]

    for idx, country in enumerate(countries.index):
        color = px.colors.qualitative.Alphabet[idx % len(
            px.colors.qualitative.Alphabet)]
        country_data = data[data['location'] == country]
        fig.add_trace(go.Scatter(
            x=country_data[x_column],
            y=country_data[y_column_1],
            mode='lines',
            line={'dash': 'solid', 'color': color},
            name=f"{country}, <br>{attr1_label}"),
            secondary_y=False)
        fig.add_trace(go.Scatter(
            x=country_data[x_column],
            y=country_data[y_column_2],
            mode='lines',
            opacity=0.3,
            line={'dash': 'solid', 'color': color},
            name=f"{country}, <br>{attr2_label}"),
            secondary_y=True)
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
    )
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return fig


def render_two_lines(df, y_column_1, y_column_2, x_column):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    attr1_label = get_our_world_in_data_attributes[y_column_1]["label"]
    attr2_label = get_our_world_in_data_attributes[y_column_2]["label"]
    date_label = get_our_world_in_data_attributes[x_column]["label"]
    fig.add_trace(go.Scatter(
                  x=df[x_column],
                  y=df[y_column_1],
                  mode='lines',
                  name=attr1_label),
                  secondary_y=False)
    fig.add_trace(go.Scatter(
                  x=df[x_column],
                  y=df[y_column_2],
                  mode='lines',
                  name=attr2_label),
                  secondary_y=True)
    fig.update_layout(
        margin=dict(r=12, t=24, b=16),
    )
    fig.update_traces(showlegend=True)
    fig.update_xaxes(title_text=f"{date_label}")
    fig.update_yaxes(title_text=f"{attr1_label}", secondary_y=False)
    fig.update_yaxes(title_text=f"{attr2_label}", secondary_y=True)
    return fig
