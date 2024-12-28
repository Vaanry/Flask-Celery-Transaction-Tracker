# Flask-Celery Transaction Tracker

## Описание проекта

Flask-Celery Transaction Tracker — это приложение для отслеживания транзакций, включающее функционал создания криптовалютных кошельков с использованием библиотеки `tronpy`. Приложение реализовано с использованием Flask для обработки HTTP-запросов и Celery для выполнения фоновых задач.

## Основные возможности
- Отслеживание статуса транзакций.
- Автоматическое обновление статуса транзакций (например, смена на "expired" для истекших).
- Создание криптовалютных кошельков через Tron blockchain.
- Вебхуки для уведомления внешних сервисов о статусе транзакций.
- Админка с автообновляемым дашбордом.
- Документация API с использованием Swagger.

## Требования

- Python 3.10+
- Flask
- Celery
- Redis (в качестве брокера и бэкенда)
- Tronpy

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone git@github.com:Vaanry/Flask_celery_test_task.git
    cd Flask_celery_test_task
    ```

2. Установите зависимости:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Настройте Redis:
    Убедитесь, что Redis запущен и доступен по адресу `127.0.0.1:6379`.

4. Настройте переменные окружения в `.env` файле:
    ```env
    DATABASE_URI=your database url
    SECRET_KEY=your secret key
    PRIVATE_KEY=private key of a previously created wallet with a non-zero balance
    ```

## Запуск приложения

1. Запустите Flask-приложение:
    ```bash
    flask run
    ```

2. Запустите Celery worker:
    ```bash
    celery -A app.celery.celery_app worker --loglevel=info
    ```

3. Запустите Celery beat:
    ```bash
    celery -A app.celery_beat beat --loglevel=info
    ```

## Структура проекта
```plaintext
project/
├── app/
│   ├── __init__.py          # Инициализация Flask-приложения
│   ├── celery.py            # Настройки Celery
│   ├── celery_beat.py       # Конфигурация периодических задач Celery beat
│   ├── tasks.py             # Определение задач Celery
│   ├── admin.py             # Конфигурация админ-панели Flask
│   ├── cli_commands.py      # Дополнительные команды для Flask CLI
│   ├── config.py            # Конфигурация приложения
│   ├── utils.py             # Утилиты для работы с TronPy
│   ├── forms.py             # Определение форм
│   ├── views.py             # Определение маршрутов (роутеров)
│   ├── models.py            # Определение моделей базы данных
│   ├── swagger.yaml         # Документация Swagger
│   ├── templates/           # Шаблоны приложения
│   │   └── admin/           # Шаблоны для админ-панели
│   └── static/              # Статические файлы приложения
├── .env                     # Переменные окружения
└── requirements.txt         # Зависимости проекта
```

## Основные команды

- **Запуск Flask**: `flask run`
- **Создание дефолтного админа: `create-admin`
- **Запуск Celery worker**: `celery -A app.celery.celery_app worker --loglevel=info`
- **Запуск Celery beat**: `celery -A app.celery_beat beat --loglevel=info`

## Примечания
- Убедитесь, что Redis запущен и доступен перед запуском Celery worker и beat.
- При необходимости вы можете настроить дополнительное логирование или изменить временные интервалы для Celery beat в `celery_beat.py`.


