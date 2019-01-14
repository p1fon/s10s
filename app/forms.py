from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

stateX = None

class EditProfileForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Отправить')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.date).first()
            if user is not None:
                raise ValidationError('Пожалуйста, выберете другое имя')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired() ,Length(min=0, max=10)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=0, max=12)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя занято')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email уже использован')

class NewsCreatorForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    body = TextAreaField('Текст новости', validators=[Length(min=0, max=720)])
    img = StringField('Прямая ссылка на картинку', validators=[Length(min=0, max=720)])
    if stateX==0: submit = SubmitField('Опубликовать')
    else: submit = SubmitField('Сохранить изменения')
    def __init__(self, stateX, *args, **kwargs):
        super(NewsCreatorForm, self).__init__(*args, **kwargs)
        self.stateX = stateX
