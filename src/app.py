from dash import Dash, html, dcc, page_container

app = Dash(__name__, use_pages=True)

app.layout = html.Div(page_container, id="root")

if __name__ == '__main__':
    print("----------> [ Please make sure you have run the pipeline before running the app in dev mode. ] <----------")

    # * The debug=True flag is used to enable hot reloading
    app.run_server(debug=True)
