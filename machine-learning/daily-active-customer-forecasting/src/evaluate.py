
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from features import create_forecasting_features


# Configuration
from config import (
    DATA_PATH,
    FEATURES,
    MODEL_PATH,
    TEST_START_DATE,
)

# Load data
def load_test_data():
    """Load and prepare the untouched November-December test data."""

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    df = df.sort_values("date")
    df = df.set_index("date")

    model_data = create_forecasting_features(df)

    # Keep only the independent test period
    test_data = model_data.loc[
    model_data.index >= TEST_START_DATE
]

    X_test = test_data[FEATURES]
    y_test = test_data["active_customers"]

    return X_test, y_test


# Evaluate model
def evaluate_model():
    """Load the saved model and evaluate it on the test period."""

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Load test data
    X_test, y_test = load_test_data()

    # Generate predictions
    predictions = model.predict(X_test)

    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    print(f"Test observations: {len(X_test)}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")



# Run evaluation pipeline
if __name__ == "__main__":
    evaluate_model()