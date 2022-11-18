import plotly.express as px

def render_map(data, color_column, country_code=None):
  return px.choropleth(
    data, locations="iso_code",
    color=color_column, # lifeExp is a column of gapminder
    hover_name="iso_code", # column to add to hover information
    color_continuous_scale=px.colors.sequential.Plasma
  )