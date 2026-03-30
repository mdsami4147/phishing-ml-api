from multiprocessing import reduction

from flask import Flask, request, jsonify
import numpy as np
import os
import joblib

app = Flask(__name__)

try:
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
        print("Model loaded successfully")
    else:
        print("model.pkl NOT FOUND")
        model = None
except Exception as e:
    print("Model load error:", e)
    model = None
def extract_features(url):

    url = url.lower()

    return [[
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        url.count('//'),
        url.count('='),
        1 if "login" in url else 0,
        1 if "secure" in url else 0,
        1 if "verify" in url else 0,
        1 if "account" in url else 0,
        1 if "update" in url else 0,
        1 if "bank" in url else 0,
        1 if "paypal" in url else 0
    ]]
    return [features]
@app.route("/")
def home():
    return "phishing ML API Running successfully"

@app.route("/predict", methods=["POST"])
def predict():
 data = request.get_json()
url = data["url"]

features = extract_features(url)

prediction = model.predict(features)[0]
probability = model.predict_proba(features)[0][1]

confidence = round(probability * 100, 2)

if confidence < 30:
    confidence = round(confidence * 0.8, 2)
elif confidence > 80:
    confidence = round(confidence * 1.05, 2)

confidence = min(confidence, 99.9)

if prediction == 1:
    result = "Phishing Website"
else:
    result = "Legitimate Website"

return jsonify({
    "result": result,
    "confidence": confidence
})
if model is None:
    return jsonify({
        "error": "Model not loaded"
    })