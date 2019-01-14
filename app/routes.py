from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, NewsCreatorForm
from flask_login import current_user, login_user, logout_user
from app.models import User, News
from flask_login import login_required
from werkzeug.urls import url_parse
from datetime import datetime

bposts = [
    { 'body': 'Test post#1'},
    { 'body': 'Test post#2'}
]
"""
@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Изменить профиль', form=form)
"""
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, posts=posts)

@app.route('/')
@app.route('/index')
def index():
    newsdata = News.query.order_by(News.timestamp.desc())
    return render_template('index.html', title='Новости', bposts=newsdata)

@app.route('/del_news/<del_id>')
@login_required
def del_news(del_id):
    if del_id!=None and current_user.username == 'admin':
        del_news = News.query.filter_by(id=del_id).first_or_404()
        db.session.delete(del_news)
        db.session.commit()
        flash('Публикация удалена')
        return redirect(url_for('index'))

@app.route('/red_news/<red_id>', methods=['GET','POST'])
@login_required
def red_news(red_id):
    if red_id!=None and current_user.username == 'admin':
        red_news = News.query.filter_by(id=red_id).first_or_404()
        form = NewsCreatorForm(1)
        if form.validate_on_submit():
            #присваивание новости значений из форм
            News.query.filter_by(id=red_id).first_or_404().title = form.title.data
            News.query.filter_by(id=red_id).first_or_404().body = form.body.data
            News.query.filter_by(id=red_id).first_or_404().img = form.img.data
            db.session.commit()
            flash('Изменения сохранены')
            return redirect(url_for('index'))
        elif request.method == 'GET':
            #присваивание формам значение из базы данных
            form.title.data = News.query.filter_by(id=red_id).first_or_404().title
            form.body.data = News.query.filter_by(id=red_id).first_or_404().body
            form.img.data = News.query.filter_by(id=red_id).first_or_404().img
        return render_template('news.html', title='Изменить новость', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрированы')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
"""
@app.route('/news_creator', methods=['GET','POST'])
@login_required
def news_creator():
    form = NewsCreatorForm(0)
    if form.validate_on_submit():
        news = News(title=form.title.data, body=form.body.data, img=form.img.data)
        db.session.add(news)
        db.session.commit()
        flash('Новость опубликована')
        redirect(url_for('news_creator'))
    #elif request.method == 'GET':
        #form.username.data = current_user.username
        #form.about_me.data = current_user.about_me"""
    return render_template('news.html', title='Редактор новостей', form=form)
