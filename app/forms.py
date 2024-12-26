from flask_wtf import FlaskForm
from wtforms import (DecimalField, PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import URL, DataRequired, Length, NumberRange


class UserForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(3, 20)],
    )
    password = PasswordField(
        "Password",
        validators=[],
    )
    balance = DecimalField("Balance", validators=[DataRequired(), NumberRange(min=0)])

    commission_rate = DecimalField(
        "Commission Rate", validators=[DataRequired(), NumberRange(min=0, max=1)]
    )
    webhook_url = StringField("Webhook URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя")
    password = PasswordField("Введите пароль")
    submit = SubmitField("Войти")


class TransactionForm(FlaskForm):
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0)])
    commission = DecimalField(
        "Commission", validators=[DataRequired(), NumberRange(min=0)]
    )
    status = SelectField(
        "Status",
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("canceled", "Canceled"),
            ("expired", "Expired"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")
