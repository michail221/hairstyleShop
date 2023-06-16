from sched import Event
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from app import app,db
from flask import Flask,redirect, flash
from app.forms import LoginForm
from app.forms import RegForm, DelItem
from app.forms import NewItem, NewOrder
from flask_login import LoginManager
from flask_login import logout_user,current_user,login_user
from app.models import User, Item , Order
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = {'username': 'Miha2002'}
    items = Item.query.order_by(Item.price).all()[:3]
    form = DelItem()
    if form.validate_on_submit():
        item = Item.query.get(form.id.data)
        db.session.delete(item)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('index.html', title='Home', user=user, data=items, form=form)
@app.route('/logout')
def logout():
     logout_user()
     return redirect('index')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/documn1')
def documn1():
    return render_template("documn1.html")

@app.route('/documn2')
def documn2():
    return render_template("documn2.html")

@app.route('/documn3')
def documn3():
    return render_template("documn3.html")

@app.route('/goog')
def goog():
    return render_template("goog.html")

@app.route('/spisok', methods=['GET', 'POST'])
def spisok():
    return render_template("spisok.html")



@app.route('/katalog', methods=['GET', 'POST'])
def katalog():
    items = Item.query.order_by(Item.price).all()
    form = DelItem()
    if form.validate_on_submit():
        item = Item.query.get(form.id.data)
        db.session.delete(item)
        db.session.commit()
        return redirect('/index')
    else:
     return render_template("katalog.html", data=items, form=form)



@app.route('/GetImage/<int:id>/<int:number>', methods=['GET', 'POST'])
def GetImage(id,number):
    items = Item.query.get(id)
    if number == 1 :
        return items.mainPhoto
    if number == 2 :
        return items.secondPhoto
    if number == 3 :
        return items.thirdPhoto

@app.route('/order/<int:id>', methods=['GET', 'POST'])
def order(id):
    items =  Item.query.get(id)
    form = NewOrder()
    if form.validate_on_submit():
        order = Order(data=form.data.data)
        return redirect('spisok.html')
        #try:
            #db.session.add(order)
            #db.session.commit()
       #    return redirect('index.html')
       # except:
        #    return "Получилась ошибка"

    else:
        return render_template("order.html", el=items, form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = NewItem()
    if form.validate_on_submit():
        item = Item(title=form.title.data, price=form.price.data, descrip=form.descrip.data, mainPhoto=form.mainPhoto.data.read(), secondPhoto=form.secondPhoto.data.read(), thirdPhoto=form.thirdPhoto.data.read())
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html', title='Добавление прически', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('index')
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data.replace(' ', '')
        user = User.query.filter_by(username=name).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователся или пароль')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = ('index')
        return redirect(next_page)
        return redirect('index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect('index')
    form = RegForm()
    if form.validate_on_submit():
        name = form.username.data.replace(' ', '')
        user = User(username=name, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем с регистрацией!',"success")
        return redirect('login')
    return render_template('reg.html', title='Register', form=form)

