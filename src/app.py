from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.BOOTSTRAP], meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
])

app.layout = html.Div(page_container, id="root")

if __name__ == '__main__':
    print(
        "----------> [ Please make sure you have run the pipeline before running the app in dev mode. ] <----------"
    )

    # * The debug=True flag is used to enable hot reloading
    app.run_server(debug=True)
