import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_data(df):

    print("\n" + "="*60)
    print("DATA PREPROCESSING")
    print("="*60)

    # Remove Student_ID
    if "Student_ID" in df.columns:
        df = df.drop("Student_ID", axis=1)
        print("✓ Student_ID removed")

    # Check missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Encode categorical columns
    encoder = LabelEncoder()

    categorical_columns = [
        "Gender",
        "Degree",
        "Branch",
        "Placement_Status"
    ]

    for col in categorical_columns:
        df[col] = encoder.fit_transform(df[col])
        print(f"✓ Encoded {col}")

    print("\nPreprocessing Completed Successfully!")

    return df