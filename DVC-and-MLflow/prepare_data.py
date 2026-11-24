# Creates data/train.csv. Usage: python prepare_data.py 1   (or 2)
# Version 1 = first 400 rows, Version 2 = full dataset (simulates "new rows arrived",
# like the 500-new-rows step in DVCexample.docx).
# To use your own dataset (diabetes, lung cancer...), replace the sklearn lines with:
#   df = pd.read_csv("your_file.csv")   and make sure the label column is named "label"
import sys, os
import pandas as pd
from sklearn.datasets import load_breast_cancer

version = sys.argv[1]

data = load_breast_cancer(as_frame=True)
df = data.frame.rename(columns={"target": "label"})

if version == "1":
    df = df.iloc[:400]

os.makedirs("data", exist_ok=True)
df.to_csv("data/train.csv", index=False)
print(f"Wrote data/train.csv for version {version}: {len(df)} rows")
