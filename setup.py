#!/usr/bin/env python3
from distutils.core import setup

setup(
    name='rushing',
    version='1.0',
    description='NFL Rushing',
    author='Adarsh Melethil',
    author_email='adarshmelethil@gmail.com',
    package_dir={"": "."},
    packages=["rushing"],
    install_requires=[
        "docopt==0.6.2",
        "Flask==1.1.2",
        "Flask-Migrate==2.7.0",
        "Flask-SQLAlchemy==2.5.1",
        "pandas==1.2.4",
        "psycopg2==2.8.6",
        "dash==1.20.0",
        "dash-core-components==1.16.0",
        "dash-html-components==1.1.3",
        "dash-table==4.11.3",
        "dash-bootstrap-components==0.12.0",
    ],
    entry_points={
        'console_scripts': ['rushing=rushing.entrypoint:main'],
    }
)
