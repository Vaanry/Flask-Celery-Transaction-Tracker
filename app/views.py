from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, session)
from werkzeug.security import check_password_hash

from .forms import LoginForm
from .models import Transaction, User, db

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        user = User.query.filter_by(username=username).first_or_404()
        if check_password_hash(user.password, form.password.data):
            session["login"] = True
            session["username"] = user.username
            session["id"] = user.id
            session["is_admin"] = user.is_admin
            flash("Вы успешно вошли в систему!", "success")
        else:
            flash("Неверный логин или пароль!", "danger")
            return render_template("login.html", form=form)
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout/")
def logout():
    session.clear()
    flash("Вы вышли из системы!", "success")
    return redirect("/")


@app.route("/create_transaction/", methods=["POST"])
def create_transaction():
    data = request.get_json()
    amount = data.get("amount")
    user_id = session.get("id")
    user = User.query.get_or_404(user_id)
    if user:
        commission_rate = user.commission_rate
        commission = amount * commission_rate
        transaction = Transaction(amount=amount, commission=commission, user_id=user_id)
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"transaction": transaction.to_dict()}), 201
    else:
        abort(403)


@app.route("/cancel_transaction/<int:id>", methods=["POST"])
def cancel_transaction(id):

    user_id = session.get("id")
    user = User.query.get_or_404(user_id)
    if user:
        transaction = Transaction.query.get_or_404(id)
        transaction.status = "canceled"
        db.session.commit()
        return jsonify({"transaction": transaction.to_dict()}), 201
    else:
        abort(403)


@app.route("/check_transaction/<int:id>")
def check_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return jsonify({"transaction": transaction.to_dict()}), 200


@app.errorhandler(403)
def render_forbidden(error):
    return render_template(
        "error.html", error="У вас нет прав для просмотра этой страницы"
    )


@app.route("/webhook", methods=["POST"])  # Временный эндпойнт для тестирования вебхуков
def webhook():
    data = request.json  # Получаем JSON данные из запроса
    print(f"Received webhook data: {data}")

    return jsonify({"message": "Webhook received successfully!"}), 200
