from . import celery_app
import time

@celery_app.task
def return_statement(statement):
    time.sleep(5)
    return statement

@celery_app.task
def scheduled_set(key,value,store):
    store.set(key,value)