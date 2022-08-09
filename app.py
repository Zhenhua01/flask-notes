"""Flask app for flask notes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Notes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)