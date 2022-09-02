from distutils.debug import DEBUG
from decouple import config

class BaseConfig(object):
    DEBUG = False
    UPLOAD_FOLDER = 'tmp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config("SECRET_KEY")


class DevConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    psql_username = config("POSTGRES_USERNAME")
    psql_password = config("POSTGRES_PASSWORD")
    psql_database = config("POSTGRES_DATABASE")
    psql_host = config("POSTGRES_HOSTNAME")
    SQLALCHEMY_DATABASE_URI = f'postgresql://{psql_username}:{psql_password}@{psql_host}:5432/{psql_database}'


class ProdConfig(BaseConfig):
    psql_username = config("POSTGRES_USERNAME")
    psql_password = config("POSTGRES_PASSWORD")
    psql_database = config("POSTGRES_DATABASE")
    psql_host = config("POSTGRES_HOSTNAME")
    SQLALCHEMY_DATABASE_URI = f'postgresql://{psql_username}:{psql_password}@{psql_host}:5432/{psql_database}'
