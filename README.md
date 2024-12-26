# Flask_celery_test_task

    ```bash
    flask run
    celery -A app.celery.celery_app  worker --loglevel=info
    celery -A app.celery_beat beat --loglevel=info
    ```
