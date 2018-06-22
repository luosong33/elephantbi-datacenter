from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

celery_ = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery = Celery(app.name,
#              broker='redis://127.0.0.1:6379/0',
#              backend='redis://127.0.0.1:6379/0')
celery_.conf.update(app.config)