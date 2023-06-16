from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_wtf.file import *
from app.models import User
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2,max=14,message="Имя пользователся должно быть от 2 до 14 символов")])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=3,max=20,message="Пароль должен быть от 4 до 20 символов")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2,max=14,message="Пароль должен быть от 2 до 14 символов")])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4,max=20,message="Пароль должен быть от 4 до 20 символов")])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email("Некорректный Email ")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя пользователя уже занято, пожалуйста используйте другое .')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес электронной почты.')

class NewItem(FlaskForm):
    title = StringField('Имя товара', validators=[DataRequired(), Length(min=2,max=14,message="Имя товара должно состоять минимум из 2 букв")])
    descrip = StringField('Описание товара', validators=[DataRequired(), Length(min=2,max=100,message="Описание должено быть от 5 до 100 символов")])
    price = IntegerField('Цена товара', validators=[DataRequired(),NumberRange(min=0,max=10000,message="Цена не может быть меньше 0")])
    mainPhoto = FileField('Главное фото',validators=[DataRequired(),FileAllowed(['png', 'jpeg', 'jpg'], 'Недопустимый формат файла')])
    secondPhoto = FileField('Второе фото',validators=[DataRequired(),FileAllowed(['png', 'jpeg', 'jpg'], 'Недопустимый формат файла')])
    thirdPhoto = FileField('Третье фото',validators=[DataRequired(),FileAllowed(['png', 'jpeg', 'jpg'], 'Недопустимый формат файла')])
    submit = SubmitField('Загрузить')

class NewOrder(FlaskForm):
    data = DateField('Дата стрижки',validators=[DataRequired()])
    time = TimeField('Дата стрижки',validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')

    def validate_data(self,data):
        if data >= datetime.now():
            user = User.query.filter_by(data=data.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста используйте другую дату')


class DelItem(FlaskForm):
    id = HiddenField("")
    submit = SubmitField('Удалить')