import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Example dataset (expand if needed)
data = {
    "url_length": [20, 60, 70, 25],
    "dots": [1, 3, 4, 1],
    "hyphen": [0, 2, 3, 0],
    "at": [0, 0, 1, 0],
    "double_slash": [1, 1, 1, 1],
    "equals": [0, 1, 0, 0],
    "login": [0, 1, 1, 0],
    "secure": [0, 1, 0, 0],
    "verify": [0, 0, 1, 0],
    "account": [0, 1, 0, 0],
    "update": [0, 1, 0, 0],
    "bank": [0, 0, 1, 0],
    "paypal": [0, 1, 0, 0],
    "label": [0, 1, 1, 0]
}

df = pd.DataFrame(data)

X = df.drop("label", axis=1)
y = df["label"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("✅ Model trained with 13 features!")