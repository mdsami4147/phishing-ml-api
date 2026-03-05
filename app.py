from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")


def extract_features(url):

    features = [
        len(url),
        url.count('.'),
        url.count('-'),
        1 if "login" in url.lower() else 0,
        1 if "secure" in url.lower() else 0,
        1 if "verify" in url.lower() else 0,
        1 if "account" in url.lower() else 0
    ]

    return [features]


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()
    url = data["url"]

    features = extract_features(url)

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    confidence = round(probability * 100, 2)

    if prediction == 1:
        result = "Phishing Website"
    else:
        result = "Legitimate Website"

    return jsonify({
        "result": result,
        "confidence": confidence
    })