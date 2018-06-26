from flask import current_app
from celery import Celery


celery = Celery(current_app.name, broker=current_app.config['CELERY_BROKER_URL'])
celery.conf.update(current_app.config)