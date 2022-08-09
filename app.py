"""Flask app for flask notes"""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_wtf import FlaskForm
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET'
connect_db(app)
db.create_all()

@app.get('/')
def homepage():
    """Redirects to registration page"""

    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def register_new_user():
    """Shows registration form, updates database, and redirects to secrete page"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username,password,email,first_name,last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            flash('username/email already taken!')
            return render_template("register.html", form=form)


        session["username"] = new_user.username
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login_user():
    """Shows login form. Authenticates user and redirect to secret"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)

