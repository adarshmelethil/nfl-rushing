import os
from os import environ as env
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or \
        f"postgresql://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}@{env['POSTGRES_HOST']}:{env['POSTGRES_PORT']}/{env['POSTGRES_DB']}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
