from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.chromedriverinit import BrowserDriverInit

app = Flask(__name__)
app.secret_key = 'secretkeyhardcoded'

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import routes, models