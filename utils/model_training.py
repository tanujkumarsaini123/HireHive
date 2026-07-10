from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import pandas as pd
import joblib

def train_model(df):

    print("\n" + "="*60)
    print("RANDOM FOREST MODEL TRAINING")
    print("="*60)

    # Features
    X = df.drop("Placement_Status", axis=1)

    # Target
    y = df["Placement_Status"]

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print(f"\nTraining Samples : {len(X_train)}")
    print(f"Testing Samples  : {len(X_test)}")

    # Random Forest
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        max_depth=10
    )

    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy : {accuracy*100:.2f}%")

    print("\nClassification Report")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    # Cross Validation
    cv_scores = cross_val_score(model, X, y, cv=5)

    print("\nCross Validation Scores")
    print(cv_scores)

    print(f"\nAverage CV Accuracy : {cv_scores.mean()*100:.2f}%")

    # Feature Importance
    importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print("\nTop Important Features")
    print(importance)

    # Save Model
    joblib.dump(model, "models/placement_model.pkl")

    print("\n✅ Random Forest model saved successfully!")

    return model