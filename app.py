from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def detect_phishing(url):
    keywords = ['login', 'verify', 'secure', 'account', 'update']
    for k in keywords:
        if k in url.lower():
            return "Phishing Website"
    return "Legitimate Website"

@app.route('/')
def home():
    return "ML API is running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify({"result": detect_phishing(data['url'])})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)