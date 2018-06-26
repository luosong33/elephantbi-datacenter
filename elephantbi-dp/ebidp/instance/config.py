# capitalize
CELERY_IMPORTS = ("import_api")
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_TASK_RESULT_EXPIRES = 300

HBASE_HOST = "localhost"
HBASE_PORT = 9090
TIMEOUT = None
AUTOCONNECT = True
TABLE_PREFIX = None
COMPAT = '0.98'
TRANSPORT = "buffered"
PROTOCOL = "binary"