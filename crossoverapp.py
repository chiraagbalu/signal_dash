import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

"""
from helpers import (
    get_default_implied_vol,
    get_default_strike_price,
    get_default_spot_price,
    get_default_expiry_weeks,
    get_default_initial_investment,
)
from deepdao import get_assets, get_aum, get_dao_graph, get_uddy_stats
from graphs import heatmap, simulation, tear_sheet
from deepdao import get_assets
"""


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    # use_pages=True,
)


app.title = "Multi Factor Model: Crossover Signal"
server = app.server


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2(children="Multi Factor Model: Crossover Signal"),
                html.Div(
                    children=[
                        html.Div(
                            html.Iframe(
                                srcDoc="""
                                <!-- TradingView Widget BEGIN -->
                                <div class="tradingview-widget-container">
                                <div id="tradingview_44e81", style="height: 370px;"></div>
                                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                                <script type="text/javascript">
                                new TradingView.widget(
                                {
                                "autosize": true,
                                "symbol": "FTX:BTCUSDT",
                                "timezone": "Etc/UTC",
                                "theme": "dark",
                                "style": "2",
                                "locale": "en",
                                "toolbar_bg": "#f1f3f6",
                                "enable_publishing": true,
                                "hide_top_toolbar": false,
                                "range": "8M",
                                "allow_symbol_change": true,
                                "studies": [
                                    "HV@tv-basicstudies"
                                ],
                                "container_id": "tradingview_44e81"
                                }
                                );
                                </script>
                                </div>
                                <!-- TradingView Widget END -->""",
                                width="100%",
                                height="400px",
                                style={
                                    "margin-top": "21px",
                                    "margin-bottom": "0px",
                                    "scrolling": "no",
                                    "frameborder": "0",
                                    "border": "none",
                                    "overflow": "hidden",
                                    "align": "center",
                                },
                                className="six columns all",
                            )
                        ),
                    ],
                    className="row",
                ),
            ]
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(port=8051, debug=True)
