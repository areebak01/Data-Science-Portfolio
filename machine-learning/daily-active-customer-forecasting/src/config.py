from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "daily_activity.csv"

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "xgboost_model.joblib"


# Model configuration
RANDOM_STATE = 42

TRAIN_END_DATE = "2023-10-31"
TEST_START_DATE = "2023-11-01"


# Model features
FEATURES = [
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