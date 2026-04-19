import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load your dataset
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Use URL column + label column
# Change names if needed
url_col = "URL"
label_col = "label"


def extract_features(url):
    url = str(url).lower()

    return [
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
    ]


X = df[url_col].apply(extract_features).tolist()
y = df[label_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=18,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy :", round(accuracy_score(y_test, pred) * 100, 2), "%")
print("Precision:", round(precision_score(y_test, pred) * 100, 2), "%")
print("Recall   :", round(recall_score(y_test, pred) * 100, 2), "%")
print("F1 Score :", round(f1_score(y_test, pred) * 100, 2), "%")

joblib.dump(model, "model.pkl")

print("✅ Accurate model saved")