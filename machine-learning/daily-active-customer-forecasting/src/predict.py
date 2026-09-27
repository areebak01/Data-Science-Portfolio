import joblib
import pandas as pd

from features import create_forecasting_features


# Configuration
from config import DATA_PATH, FEATURES, MODEL_PATH


# Load data
def load_data():
    """Load the historical daily activity dataset."""

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    df = df.sort_values("date")
    df = df.set_index("date")

    return df


# Historical predictions
def generate_predictions():
    """Generate predictions for existing historical observations."""

    model = joblib.load(MODEL_PATH)

    df = load_data()

    model_data = create_forecasting_features(df)

    X = model_data[FEATURES]

    predictions = model.predict(X)

    results = pd.DataFrame(
        {
            "actual_active_customers": model_data["active_customers"],
            "predicted_active_customers": predictions,
        },
        index=model_data.index,
    )

    return results


# Next-day forecast
def forecast_next_day():
    """Generate a one-day-ahead forecast using historical information."""

    model = joblib.load(MODEL_PATH)

    df = load_data()

    # Determine the next date after the latest observation
    next_date = df.index.max() + pd.Timedelta(days=1)

    # Add an empty row for the future date
    future_df = df.copy()

    future_df.loc[next_date, "active_customers"] = float("nan")
    future_df.loc[next_date, "transaction_count"] = float("nan")

    # Create features for the future date using historical values
    future_features = create_forecasting_features(future_df)

    # Select only the row corresponding to the next date
    X_future = future_features.loc[[next_date], FEATURES]

    # Generate forecast
    prediction = model.predict(X_future)[0]

    return next_date, prediction


# Run prediction pipeline
if __name__ == "__main__":

    # Historical predictions
    results = generate_predictions()

    print("Latest historical predictions:")
    print(results.tail())

    # Future prediction
    next_date, prediction = forecast_next_day()

    print("\nNext-day forecast:")
    print(f"Date: {next_date.date()}")
    print(f"Predicted active customers: {prediction:.0f}")