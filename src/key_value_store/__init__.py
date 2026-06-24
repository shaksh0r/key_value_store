from celery import Celery

celery_app = Celery(
    'key_value_store',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['key_value_store.tasks']
)