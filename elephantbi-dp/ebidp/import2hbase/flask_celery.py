from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import platforms  #如果你不是linux的root用户，这两行没必要
platforms.C_FORCE_ROOT=True   #允许root权限运行celery
from flask import Flask

app = Flask(__name__)

def make_celery(app):
    celery = Celery('flask_celery',
             broker='redis://127.0.0.1:6379/0',
             backend='redis://127.0.0.1:6379/0',
             include=['import2hbase.tasks'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

