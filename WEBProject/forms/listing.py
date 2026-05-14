from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, EmailField, TelField, FileField
from wtforms.validators import DataRequired, Email


class ListingForm(FlaskForm):
    name = StringField('Название продукта*', validators=[DataRequired()])
    about = TextAreaField("Немного о продукте")
    email = EmailField('Адресс электронной почты*', validators=[DataRequired()])
    phone_number = TelField('Номер телефона')
    photo = FileField('Фото продукта*',
                      validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'],
                                                              'Разрешены только изображения (jpg, jpeg, png, webp)!')])

    submit = SubmitField('Отправить')