# from celery import Celery
#
# broker = 'redis://127.0.0.1:6379/0'
# backend = 'redis://127.0.0.1:6379/0'
#
# app = Celery('tasks', broker=broker, backend=backend)  #  创建Celery的实力
from ebidp.learn.celery_ import celery


@celery.task
def add(x, y):
    for _ in range(10000):
        for j in range(10000):
            i = 1
    return x + y
