import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import dash_html_components as html

import json
import pandas as pd

import operator as py_ops

from nfl import db
from nfl.models import Rushing


OPERATORS = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


# https://dash.plotly.com/datatable/filtering
def split_filter_part(filter_part):
    for operator_type in OPERATORS:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


def init_app(app):
    dash_app = dash.Dash(
        server=app,
        routes_pathname_prefix='/')

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
                columns=[{"name": col_name, "id": col_name} for col_name in Rushing.colnames()],

                page_current=0,
                page_action='custom',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[],

                filter_action='custom',
                filter_query=''
            )])

    def fetch_data(page, per_page, sort_by, filter_query):
        query = Rushing.query
        for col_name, operator_str, filter_value in map(
                split_filter_part, filter(lambda q: q, filter_query.split(" && "))):
            table_col_name = Rushing.key_to_table(col_name)

            col = getattr(Rushing, table_col_name)
            if operator_str == "contains":
                if col.type.python_type is str:
                    query = query.filter(col.ilike(f'%{filter_value}%'))
                else:
                    query = query.filter(col == filter_value)
            elif operator_str == "datestartswith":
                pass
            else:
                if col.type.python_type is not str:
                    query = query.filter(
                        getattr(py_ops, operator_str)(
                            col, filter_value))

        order_conditions = [
            getattr(
                getattr(
                    Rushing,
                    Rushing.key_to_table(s['column_id'])),
                s["direction"])()
            for s in sort_by]
        if order_conditions:
            query = query.order_by(*order_conditions)

        results = query.paginate(page=page+1, per_page=per_page).items
        return list(map(lambda p: p.to_dict(), results))

    @dash_app.callback(
        Output('data-table', 'data'),
        Output('alert-msg', 'children'),
        Input('data-table', "page_current"),
        Input('data-table', "page_size"),
        Input('data-table', "sort_by"),
        Input('data-table', "filter_query")
    )
    def update_table(*args):
        page, per_page, sort_by, filter_query = args

        return fetch_data(*args), None

    @dash_app.callback(
        Output('data-table', 'page_size'),
        Input('data-table-page-size', 'value'))
    def update_table_page_size(page_size):
        return page_size

    return app
