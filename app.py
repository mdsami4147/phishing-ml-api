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
    # Convert probability to percentage
    confidence = round(probability * 100, 2)
    # Adjust confidence ranges for realism
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