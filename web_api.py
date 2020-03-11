import os

from flask import Flask, request
import joblib

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    text = request.form['text']
    svm = joblib.load("my_classificator.pkl")
    return svm.predict(text,'G')
