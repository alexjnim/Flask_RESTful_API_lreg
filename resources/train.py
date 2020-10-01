import sqlite3
import pickle
import pandas as pd
from flask import Flask, request
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required

import os

import sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

def train_new_model():
    # df_data_1 = pd.read_csv('data/heart.csv')

    # Create a SQL connection to our SQLite database
    connection = sqlite3.connect("data/data.db")
    cur = connection.cursor()

    df_data_1 = pd.read_sql_query("SELECT * from heart", connection)
    
    # Be sure to close the connection
    connection.close()

    X_train = df_data_1.drop(columns = ['target'])
    y_train = df_data_1['target']

    # build pipeline (should be load pipeline here)
    reg = LinearRegression()

    pipeline = Pipeline([
                    ('std_scaler', StandardScaler()),
                    ('regression', reg),
                            ])

    model = pipeline.fit(X_train, y_train)
    return model



class Train(Resource):
    @jwt_required()
    def get(self):
        model = train_new_model()
        model_path_name = 'data/model.pkl'

        if os.path.isfile(model_path_name):
            os.remove(model_path_name)
        with open(model_path_name, 'wb') as file:
            pickle.dump(model, file)

        return {'message': 'model has now been retrained'}
