from dash import html
from ..nav.nav import render_nav

def three_splitter(main, right, bottom, id, **kwargs):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        main,
                        className="main"
                    ),
                    html.Div(
                        bottom,
                        className="bottom"
                    ),
                ],
                className="left-wrapper"
            ),
            html.Div(
                [
                    html.Div(
                        render_nav()
                    ),
                    html.Div(
                        right,
                        className="right"
                    )
                ],
                className="right-wrapper"
            ),
        ],
        className="three-splitter",
        id=id,
        **kwargs,
    )
