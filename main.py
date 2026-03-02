from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Simple ML-like detection logic
def detect_phishing(url):
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update']
    
    for word in suspicious_keywords:
        if word in url.lower():
            return {
                "result": "Phishing Website",
                "confidence": "High"
            }

    return {
        "result": "Legitimate Website",
        "confidence": "Medium"
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