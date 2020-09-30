from flask import Flask, request, jsonify, render_template
import pandas as pd
import json
from io import BytesIO
import numpy as np
import requests
from flask_cors import CORS
import pickle
import base64
from io import BytesIO
from PIL import Image
from svm import support_vector_machine
from DataPreprocessor import DataPreprocessor

app = Flask(__name__)
CORS(app)
# {name : model}
model = {}


@app.route("/svm/build_model", methods=['POST'])
def build_model():
    '''
    request body{
        name: model name,
        path: path to model
    }
    '''
    name = request.form['name']
    if model[name] is None:
        _model = support_vector_machine()
        model[name] = _model.load_model(request.form['path'])

    data = DataPreprocessor().getData()
    X = data.drop(['count'], axis=1).to_numpy()
    y = data['count'].to_numpy()
    model[name].train(X, y)


@app.route("/svm/predict", methods=['POST'])
def predict():
    '''
    request body{
        name: model name,
        dataX: data X
    }
    '''
    if model[request.form['name']] is None:
        ret = "model not exist"
    else:
        fitmodel = model[request.form['name']]
        pred = fitmodel.predict(request.form['dataX'])
        ret = "success"

    payload = {"pred": str(pred),
               "result": ret,
               }
    return jsonify(payload)


if __name__ == '__main__':
    # print('*loading lenet model...')
    # build_model()
    print('*starting flask app...')
    # host='0.0.0.0', port=80
    app.run(debug=True)
