import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
from xgboost import XGBClassifier
import argparse
import os

# -------------------------
# ARGUMENTS
# -------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="data/data.csv")
parser.add_argument("--run_type", type=str, default="base")  # base / tuned
args = parser.parse_args()

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(args.data_path)

# Basic preprocessing (v1 = minimal)
df.dropna(inplace=True)

# Encode categorical
for col in df.select_dtypes(include="object").columns:
    if col != "Churn":
        df[col] = LabelEncoder().fit_transform(df[col])

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------
# MODEL CONFIG
# -------------------------
if args.run_type == "base":
    model = XGBClassifier()
else:
    model = XGBClassifier(max_depth=6, learning_rate=0.1, n_estimators=200)

# -------------------------
# MLFLOW SETUP
# -------------------------
mlflow.set_experiment("mlops_assignment_model_1_data_1")

with mlflow.start_run():

    mlflow.log_param("dataset_version", "v1")
    mlflow.log_param("model", "xgboost")
    mlflow.log_param("run_type", args.run_type)

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)

    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("f1_score", f1)

    mlflow.sklearn.log_model(model, "model")

    print(f"Accuracy: {acc}, F1: {f1}")