import pandas as pd

from evidently import Report
from evidently.presets import DataDriftPreset

from config import DATA_PATH, FEATURES, PROJECT_ROOT, TRAIN_END_DATE
from features import create_forecasting_features


MONITORING_DIR = PROJECT_ROOT / "monitoring"
DRIFT_REPORT_PATH = MONITORING_DIR / "data_drift_report.html"


def monitor_data_drift():
    """
    Compare model feature distributions between the training period
    and the later simulated production period.
    """

    # Load daily activity data
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df.set_index("date").sort_index()

    # Create the same features used by the model
    featured_data = create_forecasting_features(df)

    # Reference = model training period
    reference = featured_data.loc[
        featured_data.index <= TRAIN_END_DATE,
        FEATURES,
    ].copy()

    # Current = later simulated production period
    current = featured_data.loc[
        featured_data.index > TRAIN_END_DATE,
        FEATURES,
    ].copy()

    print(f"Reference observations: {len(reference)}")
    print(f"Current observations: {len(current)}")

    # Create Evidently drift report
    report = Report(
        metrics=[
            DataDriftPreset()
        ]
    )

    snapshot = report.run(
        reference_data=reference,
        current_data=current,
    )

    # Save interactive HTML report
    MONITORING_DIR.mkdir(parents=True, exist_ok=True)
    snapshot.save_html(str(DRIFT_REPORT_PATH))

    print(f"Drift report saved to: {DRIFT_REPORT_PATH}")


if __name__ == "__main__":
    monitor_data_drift()