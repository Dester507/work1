from celery import Celery

workers = Celery('tasks', broker='pyamqp://', backend='redis://guest@localhost')


@workers.task
def add(text):
    return text.lower()
