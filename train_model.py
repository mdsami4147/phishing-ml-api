import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Example training dataset
data = {
    "url_length":[20,55,60,15,70,25,80,18],
    "has_login":[0,1,1,0,1,0,1,0],
    "num_dots":[1,3,4,1,3,1,5,1],
    "num_hyphen":[0,2,3,0,2,0,3,0],
    "label":[0,1,1,0,1,0,1,0]
}

df = pd.DataFrame(data)

X = df.drop("label",axis=1)
y = df["label"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = LogisticRegression()
model.fit(X_train,y_train)

joblib.dump(model,"model.pkl")

print("Model trained and saved!")