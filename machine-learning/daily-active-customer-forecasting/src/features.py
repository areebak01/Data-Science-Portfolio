import pandas as pd


def create_forecasting_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create leakage-safe features for one-day-ahead forecasting.

    Parameters
    ----------
    df : pd.DataFrame
        Time-series data indexed by date containing:
        - active_customers
        - transaction_count

    Returns
    -------
    pd.DataFrame
        DataFrame containing the original data and engineered
        forecasting features.
    """

    features = df.copy()

    # Historical customer activity
    for lag in [1, 2, 3, 7, 14]:
        features[f"dac_lag_{lag}"] = (
            features["active_customers"].shift(lag)
        )

    # Historical rolling statistics
    historical_dac = features["active_customers"].shift(1)

    for window in [7, 14]:
        features[f"dac_rolling_mean_{window}"] = (
            historical_dac.rolling(window).mean()
        )

        features[f"dac_rolling_std_{window}"] = (
            historical_dac.rolling(window).std()
        )

    # Historical transaction volume
    for lag in [1, 7]:
        features[f"transactions_lag_{lag}"] = (
            features["transaction_count"].shift(lag)
        )

    # Calendar features
    features["day_of_week"] = features.index.dayofweek
    features["month"] = features.index.month

    feature_columns = [
    "dac_lag_1",
    "dac_lag_2",
    "dac_lag_3",
    "dac_lag_7",
    "dac_lag_14",
    "dac_rolling_mean_7",
    "dac_rolling_std_7",
    "dac_rolling_mean_14",
    "dac_rolling_std_14",
    "transactions_lag_1",
    "transactions_lag_7",
    "day_of_week",
    "month",
    ]

    return features.dropna(subset=feature_columns)