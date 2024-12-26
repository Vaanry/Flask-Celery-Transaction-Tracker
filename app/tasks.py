from datetime import datetime, timedelta

import requests

from .celery import celery_app
from .models import Transaction, User, db
from .utils import check_balance, generate_wallet
from .views import app


@celery_app.task
def track_transactions():
    with app.app_context():
        WEBHOOK_URL = "http://127.0.0.1:5000/webhook"  #  тестовый вебхук для проверки корректности работы
        now = datetime.now()
        expiration_time = now - timedelta(minutes=15)

        expired_transactions = Transaction.query.filter(
            Transaction.status == "pending",
            Transaction.created_at < expiration_time,
        ).all()
        count = len(expired_transactions)
        for transaction in expired_transactions:
            transaction.status = "expired"
            db.session.commit()
            payload = {
                "transaction_id": transaction.id,
                "status": transaction.status,
            }
            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to send webhook: {e}")
        print(f"Expired {count} transactions and sent webhooks.")


@celery_app.task
def check_usdt():
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.wallet is None:
                user.wallet = generate_wallet()
                db.session.commit()
            user.balance = check_balance(user.wallet)
            db.session.commit()
