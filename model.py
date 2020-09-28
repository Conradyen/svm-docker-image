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

app = Flask(__name__)
CORS(app)
# {name : model}
model = {}


@app.route("/svm/build_model", methods=['POST'])
def build_model():

    ```
    request body{
        name: model name,
        path: path to model
    }
    ```
    if model[request.form['name']] is none:
        _model = support_vector_machine()
        model[name] = _model.load_model(request.form['path'])


@app.route('/svm/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


@app.route("/svm/predict", methods=['POST'])
def predict():
    ```
    request body{
        name: model name,
        dataX: data X
    }
    ```
    if model[request.form['name']] is none:
        ret = "model not exist"
    else:
        fitmodel = model[request.form['name']]
        pred = fitmodel.predict(request.form['dataX'])
        ret = "success"

    payload = {"pred": str(pred),
               "result": ret,
               }
    return jsonify(payload)


# @app.route("/svm/predict", methods=['POST'])
# def train_model():


# @app.route("/app")
# def digit_reg():

#     return render_template("paint_app.html")


if __name__ == '__main__':
    # print('*loading lenet model...')
    # build_model()
    print('*starting flask app...')
    # host='0.0.0.0', port=80
    app.run(debug=True)
