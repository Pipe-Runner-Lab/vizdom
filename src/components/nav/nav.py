from dash import html, dcc, page_registry

pages = page_registry.values()


def render_nav():
    return html.Div([
        html.Div(
            [
                dcc.Link(
                    "Explore", href="/"
                )
            ],
            className="nav-item",
        ),
        html.Div(
            [
                dcc.Link(
                    "Analyse", href="/analyse"
                )
            ],
            className="nav-item",
        ),
        html.Div(
            [
                dcc.Link(
                    "Predict", href="/predict"
                )
            ],
            className="nav-item",
        )
        # for page in pages
    ],
        className="nav-container",
        id="nav-container"
    )
