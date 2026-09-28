import pandas as pd
from sklearn.metrics import mean_absolute_error

from config import DATA_PATH, PROJECT_ROOT


PREDICTIONS_PATH = PROJECT_ROOT / "predictions" / "forecasts.csv"
MONITORING_DIR = PROJECT_ROOT / "monitoring"
PERFORMANCE_PATH = MONITORING_DIR / "performance.csv"


def monitor_performance():
    """
    Compare saved forecasts with actual observed values.
    """

    # Load forecasts produced by batch inference
    forecasts = pd.read_csv(
        PREDICTIONS_PATH,
        parse_dates=["forecast_date"],
    )

    # Load actual historical observations
    actuals = pd.read_csv(
        DATA_PATH,
        parse_dates=["date"],
    )

    actuals = actuals[
        ["date", "active_customers"]
    ].rename(
        columns={
            "date": "forecast_date",
            "active_customers": "actual_active_customers",
        }
    )

    # Match each forecast with its actual outcome
    performance = forecasts.merge(
        actuals,
        on="forecast_date",
        how="left",
    )

    # Only evaluate forecasts whose actual value is available
    evaluated = performance.dropna(
        subset=["actual_active_customers"]
    ).copy()

    if evaluated.empty:
        print("No actual outcomes are available yet.")
        return

    evaluated["absolute_error"] = (
        evaluated["actual_active_customers"]
        - evaluated["predicted_active_customers"]
    ).abs()

    mae = mean_absolute_error(
        evaluated["actual_active_customers"],
        evaluated["predicted_active_customers"],
    )

    MONITORING_DIR.mkdir(parents=True, exist_ok=True)

    evaluated.to_csv(
        PERFORMANCE_PATH,
        index=False,
    )

    print(evaluated.to_string(index=False))
    print(f"\nForecasts evaluated: {len(evaluated)}")
    print(f"Monitoring MAE: {mae:.2f}")
    print(f"Performance report saved to: {PERFORMANCE_PATH}")


if __name__ == "__main__":
    monitor_performance()