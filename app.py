"""Flask app for flask notes"""

from crypt import methods
from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, Notes
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

@app.get('/')
def homepage():
    """Redirects to registration page"""

    return redirect('/register')

@app.route('/register', methods = ['GET', 'POST'])
def register_new_user():
    """Shows registration form, updates database, and redirects to secrete page"""

