import pandas as pd
from utils.eda import perform_eda
from utils.preprocessing import preprocess_data
from utils.model_training import train_model
# ==============================
# LOAD DATASET
# ==============================

df = pd.read_csv("dataset/train.csv")

print("=" * 50)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 50)

print("\nFirst Five Rows\n")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns.tolist())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDataset Information")
print(df.info())

print("\nStatistics")
print(df.describe())
perform_eda(df)
df = preprocess_data(df)
model = train_model(df)