#!/usr/bin/env python3
"""
Usage:
  app server start [--host=<h>] [--port=<p>] [--debug]
  app data show [--path=<pth>]
  app data load [--path=<pth>]
  app -h | --help
  app --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --host=<h>    Host [default: 127.0.0.1].
  --port=<p>    Port [default: 5000].
  --path=<pth>  Path to seed data [default: rushing.json].
"""
from docopt import docopt

import pandas as pd

from flask import Flask
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import dash_html_components as html


def init_app():
    app = Flask(__name__)
    dash_app = dash.Dash(
        server=app,
        routes_pathname_prefix='/',
    )

    df = pd.read_json('/Users/adarshmelethil/work/src/github.com/adarshmelethil/nfl-rushing/rushing.json')
    # Create Dash Layout
    dash_app.layout = html.Div(
        id='dash-container',
        children=[
            'Page Size: ',
            dcc.Input(
                id='data-table-page-size',
                type='number',
                min=1,
                max=100,
                value=10
            ),
            dbc.Alert(
                id="alert-msg",
                is_open=False,
                duration=4000,
            ),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],

                page_current=0,
                page_action='custom',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[],

                filter_action='custom',
                filter_query=''
            ),
        ]
    )

    @dash_app.callback(
        Output('data-table', 'data'),
        Output('alert-msg', 'children'),
        Input('data-table', "page_current"),
        Input('data-table', "page_size"),
        Input('data-table', "sort_by"),
        Input('data-table', "filter_query")
    )
    def update_table(page_current, page_size, sort_by, filter_query):
        print(filter_query)
        dff = df
        if len(sort_by):
            dff = df.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )
        return dff.iloc[
            page_current*page_size:(page_current + 1)*page_size
        ].to_dict('records'), None

    @dash_app.callback(
        Output('data-table', 'page_size'),
        Input('data-table-page-size', 'value'))
    def update_table_page_size(page_size):
        return page_size

    return app


def start_server(**kwargs):
    init_app().run(**kwargs)


if __name__ == '__main__':
    args = docopt(__doc__)

    if args["server"]:
        if args["start"]:
            start_server(
                host=args["--host"],
                port=int(args["--port"]),
                debug=args["--debug"])
    # elif args["data"]:
    #     if args["show"]:
    #         data_show(args["--path"])
    #     elif args["load"]:
    #         data_load(args["--path"])
