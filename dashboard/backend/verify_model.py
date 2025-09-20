import joblib
import pandas as pd

model = joblib.load("models/classifier_model.pkl")

print(model.feature_names_in_)

X_train = pd.read_csv("data/train/X_train.csv")
print(list(X_train.columns), "\n")
print(X_train.dtypes, "\n")
