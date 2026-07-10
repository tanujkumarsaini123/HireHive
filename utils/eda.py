import pandas as pd

def perform_eda(df):

    print("\n" + "="*60)
    print("EXPLORATORY DATA ANALYSIS")
    print("="*60)

    # Shape
    print("\nDataset Shape:")
    print(df.shape)

    # Columns
    print("\nColumns:")
    print(df.columns.tolist())

    # Data Types
    print("\nData Types:")
    print(df.dtypes)

    # Missing Values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Duplicate Rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # Statistics
    print("\nStatistical Summary:")
    print(df.describe())

    # Target Distribution
    print("\nPlacement Status Distribution:")
    print(df["Placement_Status"].value_counts())

    print("\nEDA Completed Successfully!")