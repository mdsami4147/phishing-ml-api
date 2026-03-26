import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Example dataset (or load CSV)
data = {
    "url_length":[20,60,70,25],
    "dots":[1,3,4,1],
    "hyphen":[0,2,3,0],
    "login":[0,1,1,0],
    "label":[0,1,1,0]
}

df = pd.DataFrame(data)

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y)

# ✅ Create model BEFORE using it
model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")

print("Model trained successfully!")