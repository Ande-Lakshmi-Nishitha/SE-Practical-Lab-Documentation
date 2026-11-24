import yaml
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Get current data version from DVC
#    (the md5 hash DVC stored in the pointer file created by `dvc add`)
with open("data/train.csv.dvc") as f:
    dvc_version = yaml.safe_load(f)["outs"][0]["md5"]

# 2. Load data and split (as in MLflowtutorial.docx)
df = pd.read_csv("data/train.csv")
X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# 3. Start MLflow experiment
mlflow.set_experiment("My_First_ML_Project")

with mlflow.start_run():
    # Log the data version as a parameter
    mlflow.log_param("dataset_version", dvc_version)
    mlflow.log_param("n_rows", len(df))

    # Define and log model parameters
    n_estimators = 100
    max_depth = 3
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # Training
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_train, y_train)

    # Evaluate and log metric
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)

    # Log the model itself
    # (cloudpickle = classic .pkl format; newer MLflow versions default to skops,
    #  which rejects RandomForest trees as "untrusted" unless you whitelist them)
    mlflow.sklearn.log_model(model, "random_forest_model",
                             serialization_format="cloudpickle")

    print(f"Data version {dvc_version[:8]} | accuracy: {accuracy:.4f}")
    print("Experiment tracked in MLflow!")
