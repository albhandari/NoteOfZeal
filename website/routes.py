from website import myobj, db
from website.models import User
from flask import render_template, flash, redirect, url_for
from website.forms import LoginForm, SignupForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

@myobj.route("/")
@login_required
def mainMenu():
    return redirect(url_for('login'))

@myobj.route("/home")
@login_required
def home():
    return render_template('home.html')

@myobj.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = False)
                return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form = form)


@myobj.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@myobj.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()


    if form.validate_on_submit():
        hashedpassword = generate_password_hash(form.password.data, method = 'sha256')
        newUser = User(username = form.username.data, email = form.email.data, password = hashedpassword)
        db.session.add(newUser)
        db.session.commit()

        return '<h1>New user has been created</h1>'

    return render_template('signup.html', form = form)
