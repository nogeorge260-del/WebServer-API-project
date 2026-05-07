from flask import Flask, request, render_template, redirect, url_for
from data import db_session

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
        return render_template('registration_new.html')
    elif request.method == 'POST':
        name = request.form['name']
        surname = (request.form['last-name'])
        return redirect(url_for('main_page'))


@app.route('/main')
# @app.route('/main/<account_name>')
def main_page():
    return render_template('main_page.html')


@app.route('/main/register_listing')
def register_product():
    return render_template('register_listing.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')