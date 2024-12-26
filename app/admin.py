from datetime import date

from flask import abort, session
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash

from .models import Transaction, User, db
from .views import app

app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

admin = Admin(
    app,
    template_mode="bootstrap4",
)


class SecureBaseModelView(ModelView):
    def is_accessible(self):
        # Проверяем, есть ли пользователь в сессии
        user_id = session.get("id")
        if not user_id:
            return False

        # Получаем пользователя из базы
        user = User.query.get(user_id)
        return user.is_admin if user else False

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class DashboardView(BaseView):
    @expose("/")
    def index(self):
        total_users = User.query.count()
        total_transactions = Transaction.query.count()
        total_transaction_sum = (
            db.session.query(db.func.sum(Transaction.amount))
            .filter(Transaction.created_at >= date.today())
            .scalar()
            or 0
        )
        recent_transactions = (
            Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()
        )
        return self.render(
            "admin/dashboard.html",
            total_users=total_users,
            total_transactions=total_transactions,
            total_transaction_sum=total_transaction_sum,
            recent_transactions=recent_transactions,
        )


class UsersAdminView(SecureBaseModelView):
    column_exclude_list = ["password"]
    page_size = 50

    def edit_form(self, obj):
        """
        Убирает поле 'password' при редактировании пользователя.
        """
        form = super().edit_form(obj)
        if "password" in form:
            delattr(form, "password")  # Удаляем поле 'password' из формы
        return form

    def on_model_change(self, form, model, is_created):
        """
        Обрабатывает сохранение модели. Пароль задаётся только при создании.
        """
        if is_created:
            if not form.password.data:
                raise ValueError("Пароль обязателен для создания пользователя.")
            model.password = generate_password_hash(form.password.data)
        else:
            # Не изменяем пароль при редактировании
            model.password = User.query.get(model.id).password

        super().on_model_change(form, model, is_created)


class TransactionAdminView(ModelView):
    can_view_details = True
    can_create = False

    column_filters = ["status", "user_id"]
    form_choices = {
        "status": [
            ("confirmed", "Confirmed"),
            ("canceled", "Canceled"),
        ]
    }

    def is_accessible(self):
        # Проверяем, есть ли пользователь в сессии
        user_id = session.get("id")
        if not user_id:
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        abort(403)

    @property
    def column_list(self):
        return self.scaffold_list_columns() + ["user_id"]

    def on_form_prefill(self, form, id):
        """
        Переопределение метода для предзаполнения формы.
        Отключает редактирование статуса, если он не 'pending'.
        """
        transaction = Transaction.query.get(id)
        if transaction and transaction.status != "pending":
            form.status.render_kw = {"disabled": True}

    def get_query(self):
        # Ограничиваем транзакции текущего пользователя
        user_id = session.get("id")
        user = User.query.get(user_id)
        if user.is_admin == True:
            return self.session.query(self.model)
        return self.session.query(self.model).filter_by(user_id=user_id)

    @property
    def can_edit(self):
        user_id = session.get("id")
        user = User.query.get(user_id)
        return user.is_admin

    @property
    def can_delete(self):
        user_id = session.get("id")
        user = User.query.get(user_id)
        return user.is_admin


# Добавление вкладок
admin.add_view(DashboardView(name="Dashboard", endpoint="dashboard"))
admin.add_view(UsersAdminView(User, db.session, name="Users"))
admin.add_view(TransactionAdminView(Transaction, db.session, name="Transactions"))
