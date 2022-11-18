from dash import html

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
                className="main-bottom-wrapper"
            ),
            html.Div(
                right,
                className="right"
            ),
        ],
        className="three-splitter",
        id=id,
        **kwargs,
    )