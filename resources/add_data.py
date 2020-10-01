### this class will allow a user to upload a csv to the database for further training

import os
import csv
import sqlite3
import pandas as pd
from flask import Flask, request
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from werkzeug.utils import secure_filename

class AddCSV(Resource):
    @jwt_required()
    def post(self):

        file = request.files['file']
        filename = secure_filename(file.filename)
        path = 'data/uploads/' + filename

        if os.path.exists(path):
            return {'message' : 'this file has already been uploaded'}
        else:
            # save data from the request in a local directory if it doesn't exist yet
            file.save(path)

            connection = sqlite3.connect('./data/data.db')
            cursor = connection.cursor()
            data = pd.read_csv(path)
            data.to_sql("heart", connection, if_exists="append")
            connection.commit()
            connection.close()

        return {'message': 'successful uploaded ' + filename + ' to the database. please proceed to retrain the model if necessary'}
