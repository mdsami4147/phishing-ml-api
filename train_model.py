import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("Model Accuracy:", accuracy)
# Load dataset
df = pd.read_csv("phishing_dataset.csv")
# Separate features and label
X = df.drop("label", axis=1)
y = df["label"]
# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)
# Train model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    random_state=42
)
# Check accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)
# Save model
joblib.dump(model, "model.pkl")