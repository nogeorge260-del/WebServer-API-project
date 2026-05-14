from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, TelField, RadioField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя*', validators=[DataRequired()])
    lastname = StringField('Фамилия*', validators=[DataRequired()])
    phone = TelField('Номер телефона*', validators=[DataRequired()])
    email = EmailField('Почта*', validators=[DataRequired()])
    gender = RadioField('Пол*', choices=[
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой')
    ], validators=[DataRequired()])
    age = IntegerField('Ваш возраст*', validators=[DataRequired()])
    password = PasswordField('Пароль*', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль*', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')