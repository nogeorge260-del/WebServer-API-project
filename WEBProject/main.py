import sqlite3
import os
from flask import Flask, request, render_template, redirect, url_for
from data import users
from data import db_session
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.listing import ListingForm
from data.users import User
from data.listings import Listings
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            lastname=form.lastname.data,
            email=form.email.data,
            about=form.about.data,
            phone=form.phone.data,
            age=form.age.data,
            gender=form.gender.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        print('1')
        return redirect('/main')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/main',methods=['GET','POST'])
@app.route('/main/<page>')
def main_page(page=1):
    if request.method == 'GET':
        page = int(page)
        if page < 1:
            page = 1
        con = sqlite3.connect("db/user_listing_info.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT name, about FROM listings""").fetchall()
        counter = 0
        show = []
        for elem in result:
            if ((page - 1) * 5) <= counter < page * 5:
                show.append(elem)
            counter += 1
        while len(show) < 5:
            show.append(['Листингов больше нет', '...'])
        con.close()
        return render_template('main_page.html', listing1=show[0],
                            listing2=show[1], listing3=show[2], listing4=show[3], listing5=show[4])
    elif request.method == 'POST':
        pass


@app.route('/main/register_listing', methods=['GET', 'POST'])
def register_product():
    form = ListingForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        file = form.photo.data

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_dir = os.path.join('static', 'img', 'products')
            os.makedirs(upload_dir, exist_ok=True)
            full_path = os.path.join(upload_dir, filename)
            file.save(full_path)
            file_path = f"/static/img/products/{filename}"

        listing = Listings(
            name=form.name.data,
            about=form.about.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            photo=file_path
        )

        db_sess.add(listing)
        db_sess.commit()

        return redirect('/main')
    return render_template('register_listing.html', form=form)



if __name__ == '__main__':
    db_session.global_init("db/user_listing_info.db")
    app.run(port=8080, host='127.0.0.1', debug=True)