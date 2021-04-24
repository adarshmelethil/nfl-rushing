#!/usr/bin/env python3
"""
Usage:
  nfl server start [--host=<h>] [--port=<p>] [--debug]
  nfl data show [--path=<pth>]
  nfl data load [--path=<pth>]
  nfl -h | --help
  nfl --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --host=<h>    Host [default: 127.0.0.1].
  --port=<p>    Port [default: 5000].
  --path=<pth>  Path to seed data [default: rushing.json].
"""
from docopt import docopt

import pandas as pd
import json

from sqlalchemy.dialects.postgresql import insert

from nfl import app, db
from nfl.models import Rushing


def data_show(filepath):
    df = pd.read_json(filepath)
    print(df.head())
    print(df.dtypes)


def data_load(filepath):
    with open(filepath, "r") as fp:
        data = json.load(fp)
    print(f"Loaded data len({len(data)})")

    for d in data:
        print(f"{d['Player']} - {d['Team']} - {d['Pos']}")
        db.session.execute(
            insert(Rushing)
            .values(**Rushing.table_dict(d))
            .on_conflict_do_nothing())
        db.session.commit()


def start_server(**kwargs):
    app.run(**kwargs)


def main():
    args = docopt(__doc__)

    if args["server"]:
        if args["start"]:
            start_server(
                host=args["--host"],
                port=int(args["--port"]),
                debug=args["--debug"])
    elif args["data"]:
        if args["load"]:
            data_load(args["--path"])
        if args["show"]:
            data_show(args["--path"])
            return


if __name__ == '__main__':
    main()
