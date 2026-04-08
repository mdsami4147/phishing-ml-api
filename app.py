from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# Load model safely
try:
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print("Model load error:", e)
    model = None


# Feature extraction
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


# Home route
@app.route("/")
def home():
    return "Phishing ML API Running Successfully 🚀"


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    if model is None:
        return jsonify({"error": "Model not loaded"})

    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"})

    url = data["url"]

    features = extract_features(url)

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    confidence = round(probability * 100, 2)

    # Adjust confidence (realistic)
    if confidence < 30:
        confidence = round(confidence * 0.8, 2)
    elif confidence > 80:
        confidence = round(confidence * 1.05, 2)

    confidence = min(confidence, 99.9)

    # Risk levels
    if confidence >= 75:
        risk_level = "High"
    elif confidence >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Result
    if prediction == 1:
        result = "Phishing Website"
    else:
        result = "Legitimate Website"

    return jsonify({
        "result": result,
        "confidence": confidence,
        "risk_level": risk_level
    })


# Render port fix
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)