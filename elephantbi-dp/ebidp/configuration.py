import os
from datetime import timedelta

LOG_FILE_DIR = './local_data/logs/'


def get_db_uri(test_env=False):
    # Database
    username = os.getenv('DB_ENV_POSTGRES_USER')
    password = os.getenv('DB_ENV_POSTGRES_PASSWORD')
    host = os.getenv('DB_ENV_POSTGRES_HOST')
    port = os.getenv('DB_ENV_POSTGRES_PORT')
    database = os.getenv('DB_ENV_POSTGRES_DBNAME')

    if test_env:
        database = os.getenv('DB_ENV_POSTGRES_DBNAME_TEST')

    # Flask-SQLAlchemy
    psql_conn_str_fmt = ('postgresql://'
                         '{username}:{password}@{host}:{port}/{database}')
    database_uri = psql_conn_str_fmt.format(
        username=username,
        password=password,
        host=host,
        port=port,
        database=database
    )

    return database_uri


class BaseConfig:
    # Builtin Configuration
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200M
    SERVER_NAME = os.getenv('SERVER_NAME')
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    # Flask-JWT
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_VERIFY_EXPIRATION = os.getenv('JWT_VERIFY_EXPIRATION', True)
    JWT_EXPIRATION_DELTA = timedelta(days=os.getenv('JWT_EXPIRATION_DELTA', 30))
    JWT_AUTH_URL_RULE = os.getenv('JWT_AUTH_URL_RULE', '/auth/login')
    JWT_AUTH_URL_OPTIONS = {'methods': ['POST'], 'subdomain': '<subdomain>'}

    # Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', 25)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SUPPRESS_SEND = False

    # Pagination
    MAX_PAGINATION_SIZE = 100

    # flasgger
    SWAGGER = {
        'subdomain': '<subdomain>',
        'title': 'Flex BI API Documentation',
        'specs': [
            {
                'version': '1.0.0',
                'endpoint': 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ]
    }


class GeneralConfig(BaseConfig):
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS',
        False)

    # File uploads
    STATIC_FOLDER = './flexbi/static/'
    STATIC_FOLDER_NAME = 'static'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'csv', 'xlsx'}


class TestConfig(GeneralConfig):
    TESTING = True

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = get_db_uri(test_env=True)

    # Flask-Mail
    MAIL_SUPPRESS_SEND = True

    # Flask-JWT
    JWT_AUTH_URL_OPTIONS = {'methods': ['POST']}


class DevelopConfig(GeneralConfig):
    DEBUG = True


class ProductionConfig(GeneralConfig):
    DEBUG = False


def get_config(env='develop'):
    configs = {
        'develop': DevelopConfig,
        'production': ProductionConfig,
        'test': TestConfig,
    }
    return configs[env]
