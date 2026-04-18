from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

model = None

try:
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    model = joblib.load(model_path)
    print("Model loaded successfully")
except Exception as e:
    print("Model load error:", e)
# Feature extraction
def extract_features(url):
    url = url.lower()

    features = [
        len(url),                     # URLLength
        url.count('.'),              # dots
        url.count('-'),
        url.count('@'),
        url.count('//'),
        url.count('='),
        url.count('?'),
        url.count('&'),
        url.count('%'),
        url.count('_'),
        url.count('~'),
        url.count('#'),
        url.count('$'),
        url.count('*'),
        url.count(','),
        url.count(';'),
        url.count('+'),
        url.count('!'),
        url.count(':'),
        url.count('/'),

        1 if "login" in url else 0,
        1 if "secure" in url else 0,
        1 if "verify" in url else 0,
        1 if "account" in url else 0,
        1 if "update" in url else 0,
        1 if "bank" in url else 0,
        1 if "paypal" in url else 0,
        1 if "signin" in url else 0,
        1 if "ebay" in url else 0,
        1 if "amazon" in url else 0,

        url.startswith("https"),
        url.startswith("http"),
        url.count("www"),
        url.count(".com"),
        url.count(".net"),
        url.count(".org"),
        url.count(".xyz"),
        url.count(".ru"),
        url.count(".tk"),
        url.count(".ml"),

        sum(c.isdigit() for c in url),
        sum(c.isalpha() for c in url),
        len(set(url)),
        url.count(".."),
        url.count("---"),
        url.count("http"),
        url.count("https"),
        url.count("://"),
        url.count("php"),
        url.count("html")
    ]

    return [features]


# Home route
@app.route("/")
def home():
    return "Phishing ML API Running Successfully 🚀"
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data["url"]

        features = extract_features(url)

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        confidence = round(probability * 100, 2)

        # Adjust confidence
        if confidence < 30:
            confidence = round(confidence * 0.8, 2)
        elif confidence > 80:
            confidence = round(confidence * 1.05, 2)

        confidence = min(confidence, 99.9)

        # Risk level
        if confidence >= 75:
            risk_level = "High"
        elif confidence >= 40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        result = "Phishing Website" if prediction == 1 else "Legitimate Website"

        return jsonify({
            "result": result,
            "confidence": confidence,
            "risk_level": risk_level
        })

    except Exception as e:
        print("ERROR:", e)   # 👈 THIS WILL SHOW IN RENDER LOGS
        return jsonify({"error": str(e)}), 500
    print("Model excepts features:", model.n_features_in_)