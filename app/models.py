from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128))
    balance = db.Column(db.Float, nullable=False, default=0.0)
    commission_rate = db.Column(db.Float, nullable=False, default=0.0)
    webhook_url = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    wallet = db.Column(db.String(255), unique=True)
    user_transaction = db.relationship(
        "Transaction", backref="user_transactions", lazy=True
    )

    def __repr__(self):
        return f"<User {self.id}, Balance: {self.balance}, Commission: {self.commission_rate}, Webhook: {self.webhook_url}>"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.String(20), nullable=False, default="pending")
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )

    def __repr__(self):
        return f"<Transaction {self.id}, Amount: {self.amount}, Commission: {self.commission}, Status: {self.status}>"

    def to_dict(self):
        return dict(
            id=self.id,
            amount=self.amount,
            commission=self.commission,
            created_at=self.created_at,
            status=self.status,
        )
