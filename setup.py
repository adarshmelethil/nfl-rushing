#!/usr/bin/env python3
from distutils.core import setup

setup(
    name='nfl-rush',
    version='1.0',
    description='nfl',
    author='Adarsh Melethil',
    author_email='adarshmelethil@gmail.com',
    package_dir={"": "."},
    packages=["."],
    entry_points={
        'console_scripts': ['nfl=nfl.entrypoint:main'],
    }
)
