from flask import Flask, request, jsonify
import joblib
app = Flask(__name__)
# Load trained ML model
model = joblib.load("model.pkl")
def extract_features(url):
    return np.array([[
        len(url),
        1 if "login" in url.lower() else 0,
        url.count("."),
        url.count("-")
    ]])
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
@app.route("/")
def home():
    return "Phishing ML API Running"
@app.route("/predict",methods=["POST"])
def predict():
    data = request.get_json()
    url = data["url"]
    features = extract_features(url)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    confidence = round(probability*100,2)
    if prediction==1:
        result="Phishing Website"
    else:
        result="Legitimate Website"
    return jsonify({
        "result":result,
        "confidence":confidence
    })
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)