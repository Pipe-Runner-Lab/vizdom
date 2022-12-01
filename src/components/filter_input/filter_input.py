from dash import html
import dash_bootstrap_components as dbc
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_filter_input(id):
    return html.Div(
        [
            html.Div(
                f'Mean {get_our_world_in_data_attributes[id]["label"]}',
                className="sub-title"
            ),
            dbc.Input(
                id={
                    "type": "filter-input",
                    "index": id
                },
                placeholder="Type filter expression",
                type="text",
                style={"marginTop": "8px"}
            ),
        ]
    )
