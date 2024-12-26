from celery.schedules import crontab

from .celery import celery_app

celery_app.conf.beat_schedule = {
    "track-transactions-every-minute": {
        "task": "app.tasks.track_transactions",
        "schedule": crontab(minute="*"),
    },
    "check-usd": {
        "task": "app.tasks.check_usdt",
        "schedule": crontab(minute="*/1"),
    },
}
