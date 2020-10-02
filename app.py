import os
import csv
import sqlite3
from flask import Flask, request
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from werkzeug.utils import secure_filename

from resources.security import authenticate, identity
from resources.user import UserRegister, UserAccounts
from resources.predict import MakePrediction
from resources.train import Train
from resources.add_data import AddCSV
from resources.reset_database import ResetDatabase

# +
app = Flask(__name__)
app.secret_key = 'alex'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(MakePrediction, '/predict')
api.add_resource(Train, '/train')
api.add_resource(UserRegister, '/register')
api.add_resource(UserAccounts, '/accounts')
api.add_resource(AddCSV, '/add_csv')
api.add_resource(ResetDatabase, '/reset_database' )
# -

if __name__ == '__main__':
    from resources.db import db
    db.init_app(app)

    # this will check if data.db already exists, if not, it will run create_tables.py and create a new data.db
    if os.path.exists('data/data.db') != True:
        print('running create_tables.py')
        from resources import create_tables

    app.run(port = 5000, debug=True, use_reloader=False)
