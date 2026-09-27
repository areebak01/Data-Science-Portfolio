import sys
from pathlib import Path

import pandas as pd


# Allow imports from the src directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from features import create_forecasting_features


def test_lag_features_use_historical_values():

    """Check that lag features use past observations correctly."""

    dates = pd.date_range("2024-01-01", periods=20, freq="D")

    df = pd.DataFrame(
        {
            "active_customers": range(100, 120),
            "transaction_count": range(200, 220),
        },
        index=dates,
    )

    features = create_forecasting_features(df)

    test_date = pd.Timestamp("2024-01-20")

    # Previous day's active customers
    expected_lag_1 = df.loc["2024-01-19", "active_customers"]

    # Active customers seven days earlier
    expected_lag_7 = df.loc["2024-01-13", "active_customers"]

    # Transactions from the previous day
    expected_transactions_lag_1 = df.loc[
        "2024-01-19",
        "transaction_count",
    ]

    assert features.loc[test_date, "dac_lag_1"] == expected_lag_1

    assert features.loc[test_date, "dac_lag_7"] == expected_lag_7

    assert (
        features.loc[test_date, "transactions_lag_1"]
        == expected_transactions_lag_1
    )

def test_rolling_mean_uses_only_historical_values():
    """Check that rolling features exclude the current day's value."""

    dates = pd.date_range("2024-01-01", periods=20, freq="D")

    df = pd.DataFrame(
        {
            "active_customers": range(100, 120),
            "transaction_count": range(200, 220),
        },
        index=dates,
    )

    features = create_forecasting_features(df)

    test_date = pd.Timestamp("2024-01-20")

    # 7-day mean should use Jan 13-Jan 19,
    # excluding the current day (Jan 20)
    expected_mean = df.loc[
        "2024-01-13":"2024-01-19",
        "active_customers",
    ].mean()

    actual_mean = features.loc[
        test_date,
        "dac_rolling_mean_7",
    ]

    assert actual_mean == expected_mean

def test_features_can_be_created_for_future_date():
    """Check that features can be generated when the future target is unknown."""

    dates = pd.date_range("2024-01-01", periods=20, freq="D")

    df = pd.DataFrame(
        {
            "active_customers": range(100, 120),
            "transaction_count": range(200, 220),
        },
        index=dates,
    )

    future_date = pd.Timestamp("2024-01-21")

    # Future values are unknown at prediction time
    df.loc[future_date, "active_customers"] = float("nan")
    df.loc[future_date, "transaction_count"] = float("nan")

    features = create_forecasting_features(df)

    # The future row should survive feature engineering
    assert future_date in features.index

    # Its lag should come from the latest known observation
    assert features.loc[future_date, "dac_lag_1"] == 119

    # Current target should still be unknown
    assert pd.isna(
        features.loc[future_date, "active_customers"]
    )