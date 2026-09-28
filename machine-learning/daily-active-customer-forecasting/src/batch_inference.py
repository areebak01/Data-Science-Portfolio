import argparse

import joblib
import pandas as pd

from config import DATA_PATH, FEATURES, MODEL_PATH, PROJECT_ROOT
from features import create_forecasting_features


PREDICTIONS_DIR = PROJECT_ROOT / "predictions"
PREDICTIONS_PATH = PREDICTIONS_DIR / "forecasts.csv"


def run_batch_inference(as_of_date: str):
    """
    Generate a one-day-ahead forecast using only data available
    up to the specified as-of date.
    """

    # Load historical daily data
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.set_index("date").sort_index()

    as_of_date = pd.Timestamp(as_of_date)

    # Prevent accidental use of future observations
    available_data = df.loc[df.index <= as_of_date].copy()

    if available_data.empty:
        raise ValueError("No data is available on or before the as-of date.")

    if available_data.index.max() != as_of_date:
        raise ValueError(
            f"No observation exists for the as-of date: {as_of_date.date()}"
        )

    # The system is forecasting the following day
    forecast_date = as_of_date + pd.Timedelta(days=1)

    # Add an empty future row
    future_row = pd.DataFrame(
        {
            "active_customers": [float("nan")],
            "transaction_count": [float("nan")],
        },
        index=[forecast_date],
    )

    inference_data = pd.concat([available_data, future_row])

    # Apply the same feature engineering used during training
    featured_data = create_forecasting_features(inference_data)

    if forecast_date not in featured_data.index:
        raise ValueError(
            "Unable to create all required features for the forecast date."
        )

    X_future = featured_data.loc[[forecast_date], FEATURES]

    # Load the trained model
    model = joblib.load(MODEL_PATH)

    prediction = model.predict(X_future)[0]

    # Save forecast
    PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

    forecast = pd.DataFrame(
        {
            "as_of_date": [as_of_date.date()],
            "forecast_date": [forecast_date.date()],
            "predicted_active_customers": [round(float(prediction))],
        }
    )

    if PREDICTIONS_PATH.exists():
        existing = pd.read_csv(PREDICTIONS_PATH)
        forecasts = pd.concat([existing, forecast], ignore_index=True)

        # Avoid duplicate forecasts for the same as-of date
        forecasts = forecasts.drop_duplicates(
            subset=["as_of_date"],
            keep="last",
        )
    else:
        forecasts = forecast

    forecasts.to_csv(PREDICTIONS_PATH, index=False)

    print(f"As-of date: {as_of_date.date()}")
    print(f"Forecast date: {forecast_date.date()}")
    print(f"Predicted active customers: {round(float(prediction))}")
    print(f"Forecast saved to: {PREDICTIONS_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run one-day-ahead batch forecasting."
    )

    parser.add_argument(
        "--as-of-date",
        required=True,
        help="Latest date of data available, in YYYY-MM-DD format.",
    )

    args = parser.parse_args()

    run_batch_inference(args.as_of_date)