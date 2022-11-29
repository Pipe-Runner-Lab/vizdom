import plotly.express as px

def render_bubbles(data, attribute_1, attribute_2, color_column=None):
    fig = px.scatter(data, x=attribute_1, y=attribute_2,
	         size=10, color="iso_code",
                 hover_name=color_column)
    return fig