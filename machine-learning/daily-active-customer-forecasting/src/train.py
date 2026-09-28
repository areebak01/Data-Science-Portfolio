import mlflow
import mlflow.xgboost
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
from mlflow.models import infer_signature
from features import create_forecasting_features

# Configuration
from config import (
    DATA_PATH,
    FEATURES,
    MODEL_DIR,
    MODEL_PATH,
    RANDOM_STATE,
    TEST_START_DATE,
    TRAIN_END_DATE,
)

# Load data
def load_data():
    """Load the prepared daily customer activity dataset."""

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    df = df.sort_values("date")
    df = df.set_index("date")

    return df


# Train model
def train_model():
    """Train and save the final XGBoost forecasting model."""
    mlflow.set_experiment("daily-active-customer-forecasting")

    # Load prepared daily data
    df = load_data()

    # Create leakage-safe forecasting features
    model_data = create_forecasting_features(df)

    X = model_data[FEATURES]
    y = model_data["active_customers"]

    # Final model training period: January-October
    train_mask = X.index <= TRAIN_END_DATE
    test_mask = X.index >= TEST_START_DATE

    X_train = X.loc[train_mask]
    y_train = y.loc[train_mask]

    X_test = X.loc[test_mask]
    y_test = y.loc[test_mask]

    with mlflow.start_run():

        # Hyperparameters selected during time-series cross-validation
        model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=100,
        max_depth=1,
        learning_rate=0.03,
        min_child_weight=5,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=10.0,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        )

        # Train final model
        model.fit(X_train, y_train)

        # Evaluate on untouched test period
        predictions = model.predict(X_test)

        # Create model input/output signature
        signature = infer_signature(
        X_test,
        predictions,
        )

        # Store a small example of valid model input
        input_example = X_test.head(5)

        mae = mean_absolute_error(y_test, predictions)

        rmse = mean_squared_error(
        y_test,
        predictions
        ) ** 0.5

        # Log model hyperparameters
        mlflow.log_params(
        {
            "n_estimators": 100,
            "max_depth": 1,
            "learning_rate": 0.03,
            "min_child_weight": 5,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "reg_lambda": 10.0,
        }
        )

        # Log evaluation metrics
        mlflow.log_metrics(
        {
            "mae": mae,
            "rmse": rmse,
        }
        )

        # Log the trained model as an MLflow artifact
        mlflow.xgboost.log_model(
            model,
            name="model",
            signature=signature,
            input_example=input_example,
        )

        print(f"Training observations: {len(X_train)}")
        print(f"Test observations: {len(X_test)}")
        print(f"Test MAE: {mae:.2f}")
        print(f"Test RMSE: {rmse:.2f}")

        # Save model locally for our existing inference pipeline
        MODEL_DIR.mkdir(parents=True, exist_ok=True)

        joblib.dump(model, MODEL_PATH)

        print(f"Model saved to: {MODEL_PATH}")

# Run training pipeline
if __name__ == "__main__":
    train_model()