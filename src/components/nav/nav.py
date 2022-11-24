from dash import html, dcc, page_registry

pages = page_registry.values()

def render_nav():
    print(len(pages))

    return html.Div([
        html.Div([
            dcc.Link(
                f"{page['name']}", href=page["relative_path"]
            )
        ],
            className="nav-item",
        )
        for page in pages
    ],
        className="nav-container",
        id="nav-container"
    )
