from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os

app = Flask(__name__)
CORS(app)

model = joblib.load("model.pkl")


def extract_features(url):
    url = str(url).lower()

    return [[
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('@'),
        url.count('//'),
        url.count('='),
        url.count('?'),
        sum(c.isdigit() for c in url),
        1 if url.startswith("https") else 0,
        1 if "login" in url else 0,
        1 if "verify" in url else 0,
        1 if "secure" in url else 0,
        1 if "account" in url else 0,
        1 if "bank" in url else 0,
        1 if "paypal" in url else 0,
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    ]]


@app.route("/")
def home():
    return "AI Phishing Detector Running"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data["url"]

        features = extract_features(url)

        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        url_lower = url.lower()

        keywords = [
         "login", "verify", "secure", "update",
         "bank", "paypal", "signin", "account"
        ]

        keyword_hits = sum(word in url_lower for word in keywords)

        # Hybrid boost
        if keyword_hits >= 2:
         prob = max(prob, 0.78)

        if keyword_hits >= 4:
         prob = max(prob, 0.92)

        pred = 1 if prob >= 0.5 else 0

        confidence = round(prob * 100, 2)

        if confidence >= 75:
            risk = "High"
        elif confidence >= 40:
            risk = "Medium"
        else:
            risk = "Low"

        result = "Phishing Website" if pred == 1 else "Legitimate Website"

        return jsonify({
            "result": result,
            "confidence": confidence,
            "risk_level": risk
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)