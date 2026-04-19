import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Remove text columns
df = df.select_dtypes(include=['int64', 'float64'])

# Target
X = df.drop("label", axis=1)
y = df["label"]

# Save columns
joblib.dump(X.columns.tolist(), "columns.pkl")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Accuracy
acc = model.score(X_test, y_test)
print("Accuracy:", round(acc * 100, 2), "%")

# Save model
joblib.dump(model, "model.pkl")

print("✅ Final Pro Model Created")