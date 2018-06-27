class GeneralConfig:
    pass


class DevelopConfig(GeneralConfig):
    CELERY_IMPORTS = "import_api"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_TASK_RESULT_EXPIRES = 300

    HBASE_HOST = "localhost"
    HBASE_PORT = 9090
    TIMEOUT = None
    AUTOCONNECT = True
    TABLE_PREFIX = None
    COMPAT = "0.98"
    TRANSPORT = "buffered"
    PROTOCOL = "binary"

    DATABASE_URL = "http://localhost:8765/"

    DEBUG = True


class ProductionConfig(GeneralConfig):
    DEBUG = False


class TestConfig(GeneralConfig):
    TESTING = True


def get_config(env='develop'):
    configs = {
        'develop': DevelopConfig,
        'production': ProductionConfig,
        'test': TestConfig
    }
    return configs[env]
