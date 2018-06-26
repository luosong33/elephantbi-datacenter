from flask import current_app
from celery import Celery


celery = Celery(current_app.name, broker=current_app.config['CELERY_BROKER_URL'])
# celery = Celery(app.name,
#              broker='redis://127.0.0.1:6379/0',
#              backend='redis://127.0.0.1:6379/0')
celery.conf.update(current_app.config)