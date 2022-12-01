from dash import html
from ..nav.nav import render_nav


def app_bar():
    return html.Div([
        html.Div(
            [
                html.Div([
                    html.I(className="fa-sharp fa-solid fa-virus logo")
                ], className="logo-container"),
                html.Div("VIZDOM", className="app-title"),
            ],
            className="app-bar-left",
        ),
        html.Div(
            render_nav()
        ),
    ], className="app-bar")


def app_shell(child):
    return html.Div(
        [
            app_bar(),
            child
        ],
        className="app-shell"
    )


def three_splitter_v1(main, right, bottom, id, **kwargs):
    return app_shell(
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            main,
                            className="main"
                        ),
                        html.Div(
                            bottom,
                            className="bottom",
                        ),
                    ],
                    className="left-wrapper"
                ),
                html.Div(
                    [
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
    )


def three_splitter_v2(main_1, main_2, right, bottom, id, **kwargs):
    return app_shell(
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    main_1,
                                    className="sub-main"
                                ),
                                main_2
                            ],
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
    )
