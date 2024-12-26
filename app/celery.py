from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)

celery_app.conf.update(
    result_expires=3600,
    timezone="UTC",
    enable_utc=True,
)

celery_app.autodiscover_tasks(["app"])

# celery -A app.celery.celery_app  worker --loglevel=info
# celery -A app.celery_beat beat --loglevel=info
