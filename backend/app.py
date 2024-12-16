#!/usr/bin/env python3
"""The main entry point for the Flask application
initializes the app and sets configurations"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes import init_routes

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql+pymysql://mikonimo:8a3k5r13@localhost/campuskorner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

init_routes(app)


if __name__ == '__main__':
    app.run()
