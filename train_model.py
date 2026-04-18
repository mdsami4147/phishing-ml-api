import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

print("Original Columns:")
print(df.columns)

# Keep only numeric columns
df = df.select_dtypes(include=['int64', 'float64'])

print("Numeric Columns:")
print(df.columns)

# Make sure label exists
if "label" not in df.columns:
    raise Exception("label column missing")

# Split features + target
X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("✅ model.pkl created successfully")
print("Features used:", len(X.columns))