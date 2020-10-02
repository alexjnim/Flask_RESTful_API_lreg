import sqlite3
import os

from os import listdir
from os.path import isfile, join

import pandas as pd
from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from werkzeug.utils import secure_filename

class ResetDatabase(Resource):
    @jwt_required()
    def get(self):
        print('reseting data in the database to the original data')

        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()

        data = pd.read_csv('data/heart.csv')
        data.to_sql("heart", connection, if_exists="replace")

        connection.commit()
        connection.close()

        #here data in the uploads folder is deleted, so data has to be uploaded again to be added to the database 
        uploads_path = 'data/uploads/'
        onlyfiles = [f for f in listdir(uploads_path) if isfile(join(uploads_path, f))]

        for file in onlyfiles:
            os.remove(uploads_path+file)



        return {'message' : 'the data has been reset to the original. Please reupload the data to add to the database (the users for authentication remain the same)'}
