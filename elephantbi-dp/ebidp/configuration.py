import os
from datetime import timedelta


def get_db_uri(test_env=False):
    pass


class BaseConfig:
    pass


class GeneralConfig(BaseConfig):
    pass


class TestConfig(GeneralConfig):
    TESTING = True

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = get_db_uri(test_env=True)

    # Flask-Mail
    MAIL_SUPPRESS_SEND = True

    # Flask-JWT
    JWT_AUTH_URL_OPTIONS = {'methods': ['POST']}


class DevelopConfig(GeneralConfig):
    CELERY_IMPORTS = ("import_api")
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_TASK_RESULT_EXPIRES = 300

    HBASE_HOST = "localhost"
    HBASE_PORT = "9090"
    TIMEOUT = "None"
    AUTOCONNECT = "True"
    TABLE_PREFIX = "None"
    COMPAT = "0.98"
    TRANSPORT = "buffered"
    PROTOCOL = "binary"

    DEBUG = True


class ProductionConfig(GeneralConfig):
    DEBUG = False

def class_to_dict(obj):
    #  把对象(支持单个对象、list、set)转换成字典
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            #把Object对象转换成Dict对象
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict

def get_config(env='develop'):
    configs = {
        'develop': class_to_dict(DevelopConfig),
        'production': class_to_dict(ProductionConfig),
        'test': TestConfig,
    }
    return configs[env]
