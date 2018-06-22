from celery import Celery

broker = 'redis://127.0.0.1:6379/0'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('celery_demo', broker=broker, backend=backend)  #  创建Celery的实力