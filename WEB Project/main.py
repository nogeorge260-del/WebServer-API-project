from flask import Flask, request, render_template, redirect, url_for
from data import db_session
from data.users import User
from data.listings import Listings
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('Enter_system.html')
    elif request.method == 'POST':
        return redirect(url_for('main_page'))


@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == 'GET':
        return render_template('New Registration.html')
    elif request.method == 'POST':
        return redirect(url_for('main_page'))


@app.route('/main',methods=['GET','POST'])
#@app.route('/main/<page')
def main_page(page=1):
    if request.method == 'GET':
        con = sqlite3.connect("db/user_listing_info.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT name, about FROM listings""").fetchall()
        counter = 0
        show = []
        for elem in result:
            if counter < 5:
                show.append(elem)
            else:
                break
            counter += 1
        while counter < 5:
            show.append(['Листингов больше нет', '...'])
            counter += 1
        con.close()
        return render_template('main_page.html', listing1=show[0],
                            listing2=show[1], listing3=show[2], listing4=show[3], listing5=show[4])
    elif request.method == 'POST':
        pass


@app.route('/main/register_listing',methods=['GET','POST'])
def register_product():
    if request.method == 'GET':
        return render_template('register_listing.html')
    elif request.method == 'POST':
        ls = Listings()
        ls.name = request.form['name']
        ls.about = request.form['about']
        ls.email = request.form['email']
        print(ls.name, ls.about, ls.email)
        db_sess = db_session.create_session()
        db_sess.add(ls)
        db_sess.commit()
        return redirect(url_for('main_page'))


if __name__ == '__main__':
    db_session.global_init("db/user_listing_info.db")
    app.run(port=8080, host='127.0.0.1')