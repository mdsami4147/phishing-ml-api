from flask import Flask,request,jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

model = joblib.load("model.pkl")


def extract_features(url):

    return np.array([[
        len(url),
        1 if "login" in url.lower() else 0,
        url.count("."),
        url.count("-")
    ]])


@app.route("/")
def home():
    return "Phishing ML API Running"


@app.route("/predict",methods=["POST"])
def predict():

    data = request.get_json()
    url = data["url"]

    features = extract_features(url)

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    confidence = round(probability*100,2)

    if prediction==1:
        result="Phishing Website"
    else:
        result="Legitimate Website"

    return jsonify({
        "result":result,
        "confidence":confidence
    })


if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)