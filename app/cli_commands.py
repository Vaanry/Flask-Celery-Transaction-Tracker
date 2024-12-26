import click
from werkzeug.security import generate_password_hash

from .models import User, db
from .views import app


@app.cli.command("create-admin")
def create_admin():
    "Create a default admin user."
    admin = User(
        username="admin",
        password=generate_password_hash("admin"),
        balance=0.0,
        commission_rate=0.0,
        webhook_url="http://example.com/webhook",
        is_admin=True,
    )
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Default admin created with ID: {admin.id}")
