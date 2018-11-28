# coding:utf-8
from celery import Celery

from answer import process

app = Celery('task', broker='redis://localhost//')

@app.task
def add(x, y):
    print('on add ....')
    return x + y

@app.task
def exam(username, password):
    return process(username, password)

