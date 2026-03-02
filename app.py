from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def detect_phishing(url):
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update', 'bank', 'signin']
    
    score = 0

    # Keyword scoring
    for word in suspicious_keywords:
        if word in url.lower():
            score += 15

    # Long URL penalty
    if len(url) > 50:
        score += 10

    # Too many hyphens
    if url.count('-') > 3:
        score += 10

    # Cap score at 100
    confidence = min(score, 100)

    if confidence >= 40:
        return {
            "result": "Phishing Website",
            "confidence": confidence
        }
    else:
        return {
            "result": "Legitimate Website",
            "confidence": 100 - confidence
        }

@app.route('/')
def home():
    return "Phishing Detection ML API is Running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    prediction = detect_phishing(url)
    return jsonify(prediction)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)