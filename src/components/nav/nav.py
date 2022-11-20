from dash import html, dcc, page_registry


def render_nav():
    return html.Div([
        html.Div([
            dcc.Link(
                f"{page['name']}", href=page["relative_path"]
            )
        ],
            className="nav-item"
        )
        for page in page_registry.values()
    ],
        className="nav-container",
    )
