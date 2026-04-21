
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

        keyword_hits = sum(1 for word in keywords if word in url_lower)

        # HARD OVERRIDE
        if keyword_hits >= 4:
         pred = 1
         prob = 0.95

        elif keyword_hits >= 2:
         pred = 1
         prob = 0.85

        elif prob >= 0.5:
         pred = 1
        else:
         pred = 0
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