import os
import pandas as pd

FEATURE_DIR = "../DEAM/features/features"

sample_files = sorted(os.listdir(FEATURE_DIR))[:5]

print("Inspecting sample feature files...\n")

for fname in sample_files:
    path = os.path.join(FEATURE_DIR, fname)
    df = pd.read_csv(path, header=None)

    print(f"File: {fname}")
    print("Shape:", df.shape)

    first_row = df.iloc[0, 0]
    parts = first_row.split(";")
    print("Estimated number of features:", len(parts))
    print("First 10 features:", parts[:10])
    print("----------------------------------------")
