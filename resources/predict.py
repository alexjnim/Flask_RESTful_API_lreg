### this will load the existing model.pkl and make predictions with the json input

import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request
from flask_restful import Api, Resource

import sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

class MakePrediction(Resource):
    def post(self):
        #check if the data is json
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        posted_data = request.get_json()
        values = posted_data['input_data'][0]['values']

        #load model
        pkl_file_path = 'data/model.pkl'
        with open(pkl_file_path, 'rb') as file:
            model = pickle.load(file)

        prediction = model.predict(values)[0]

        # no need to jsonify with flask_restful
        return {'Prediction': prediction}
