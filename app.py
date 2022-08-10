"""Flask app for flask notes"""

from flask import Flask, session, render_template, redirect, flash
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, NoteForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET'
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def homepage():
    """Redirects to registration page"""

    return redirect('/register')


@app.route('/register', methods = ['GET', 'POST'])
def register_new_user():
    """Shows registration form, updates database, and redirects to secret page"""

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
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login_user():
    """Shows login form. Authenticates user and redirect to secret"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def shows_user_detail(username):
    """Shows page for logged in users only """

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    if "username" not in session or username != session['username']:
        return redirect("/login")

    return render_template("user.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        session.pop('username', None)

    return redirect("/")


@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes user instance from DB"""

    user = User.query.get_or_404(username)

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop('username', None)

        Note.query.filter_by(owner=username).delete()
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        return redirect ('/')
    else:
        return redirect(f'/users/{user.username}')


@app.route('/users/<username>/notes/add', methods = ['GET','POST'])
def add_note(username):
    """Displays add note form and adds note to username and
    redirect to user page"""

    if "username" not in session or username != session['username']:
        return redirect("/login")

    user = User.query.get_or_404(username)

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_note = Note(title=title, content=content, owner=username)
        db.session.add(new_note)
        db.session.commit()

        return redirect(f'/users/{user.username}')

    else:
        return render_template('note.html', form=form)


@app.route('/notes/<int:note_id>/update', methods = ['GET','POST'])
def edit_note(note_id):
    """Displays note form and edits note of user and
    redirect to user page"""

    note = Note.query.get_or_404(note_id)

    if "username" not in session or note.owner != session['username']:
        return redirect("/login")

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()

        return redirect(f'/users/{note.owner}')

    else:
        return render_template('note.html', form=form)


@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """Deletes note instance from DB"""

    note = Note.query.get_or_404(note_id)

    if "username" not in session or note.owner != session['username']:
        return redirect("/login")

    form = CSRFProtectForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(f'/users/{note.owner}')
    else:
        return redirect(f'/users/{note.owner}')
