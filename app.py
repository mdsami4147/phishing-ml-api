from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("model.pkl")


# -------------------------
# Feature Extraction
# -------------------------
def extract_features(url):
    url = str(url).lower()

    return [[
        len(url),                          # 1 URL length
        url.count('.'),                   # 2 dots
        url.count('-'),                   # 3 hyphens
        url.count('@'),                   # 4 @ symbol
        url.count('//'),                  # 5 //
        url.count('='),                   # 6 =
        url.count('?'),                   # 7 ?
        sum(c.isdigit() for c in url),    # 8 digits
        1 if url.startswith("https") else 0,   # 9 HTTPS
        1 if "login" in url else 0,            # 10
        1 if "verify" in url else 0,           # 11
        1 if "secure" in url else 0,           # 12
        1 if "account" in url else 0,          # 13
        1 if "bank" in url else 0,             # 14
        1 if "paypal" in url else 0,           # 15
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0  # 16 IP address
    ]]


# -------------------------
# Home Route
# -------------------------
@app.route("/")
def home():
    return "🚀 Final Perfect Phishing API Running"


# -------------------------
# Prediction Route
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "URL not provided"}), 400

        url = data["url"].strip().lower()

        # Extract features
        features = extract_features(url)

        # ML Prediction
        pred = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        # -------------------------
        # Hybrid Smart Detection
        # -------------------------
        keywords = [
            "login", "verify", "secure", "update",
            "bank", "paypal", "signin", "account",
            "password", "confirm", "wallet", "otp"
        ]

        suspicious_tlds = [".tk", ".ml", ".ru", ".xyz", ".top", ".gq"]

        keyword_hits = sum(1 for word in keywords if word in url)
        tld_hits = sum(1 for tld in suspicious_tlds if tld in url)

        has_ip = bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))
        many_hyphens = url.count('-') >= 2
        long_url = len(url) > 60

        score = keyword_hits + tld_hits

        if has_ip:
            score += 2

        if many_hyphens:
            score += 1

        if long_url:
            score += 1

        # -------------------------
        # Final Decision Override
        # -------------------------
        if score >= 4:
            pred = 1
            prob = 0.96

        elif score >= 2:
            pred = 1
            prob = max(prob, 0.85)

        else:
            pred = 1 if prob >= 0.5 else 0

        # -------------------------
        # Confidence
        # -------------------------
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


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)