import plotly.express as px
from crawlers.url_crawlers import get_our_world_in_data_attributes


def render_map(data, color_column, country_code=None, aggregation_type=None):
    fig = px.choropleth(
        data, locations="iso_code",
        color=color_column,
        hover_name="location",
        color_continuous_scale=px.colors.sequential.Peach,
        labels={
            color_column: f'{get_our_world_in_data_attributes[color_column]["label"]} ({aggregation_type})',
        }
    )

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True,
                    projection_type="natural earth")
    fig.update_layout(margin={"r": 16, "t": 0, "l": 16, "b": 0})
    return fig
