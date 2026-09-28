from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "daily_activity.csv"
PREDICTIONS_PATH = PROJECT_ROOT / "predictions" / "forecasts.csv"
PERFORMANCE_PATH = PROJECT_ROOT / "monitoring" / "performance.csv"


st.set_page_config(
    page_title="Daily Active Customer Forecasting",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    return df.sort_values("date")


@st.cache_data
def load_forecasts():
    return pd.read_csv(
        PREDICTIONS_PATH,
        parse_dates=["as_of_date", "forecast_date"],
    )


@st.cache_data
def load_performance():
    return pd.read_csv(
        PERFORMANCE_PATH,
        parse_dates=["as_of_date", "forecast_date"],
    )


df = load_data()
forecasts = load_forecasts()
performance = load_performance()


# Page header
st.title("Daily Active Customer Forecasting")

st.write(
    "An end-to-end machine learning project for forecasting daily "
    "active customers from historical transaction activity."
)

st.info(
    "This portfolio project uses a static historical dataset. "
    "Production inference and monitoring are simulated using "
    "time-based historical observations."
)


# Historical customer activity
st.subheader("Historical Customer Activity")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Historical Period",
    f"{df['date'].min().date()} to {df['date'].max().date()}",
)

col2.metric(
    "Daily Observations",
    f"{len(df):,}",
)

col3.metric(
    "Average Daily Customers",
    f"{df['active_customers'].mean():,.0f}",
)

chart_data = df.set_index("date")[["active_customers"]]

st.line_chart(chart_data)


# Batch forecasts
st.subheader("Batch Forecasts")

latest_forecast = forecasts.sort_values("forecast_date").iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "As-of Date",
    latest_forecast["as_of_date"].date().isoformat(),
)

col2.metric(
    "Forecast Date",
    latest_forecast["forecast_date"].date().isoformat(),
)

col3.metric(
    "Predicted Active Customers",
    f"{latest_forecast['predicted_active_customers']:,.0f}",
)

st.write("Recent Forecasts")

display_forecasts = forecasts.sort_values(
    "forecast_date",
    ascending=False,
).copy()

display_forecasts["as_of_date"] = (
    display_forecasts["as_of_date"].dt.strftime("%Y-%m-%d")
)

display_forecasts["forecast_date"] = (
    display_forecasts["forecast_date"].dt.strftime("%Y-%m-%d")
)

display_forecasts = display_forecasts.rename(
    columns={
        "as_of_date": "As-of Date",
        "forecast_date": "Forecast Date",
        "predicted_active_customers": "Predicted Active Customers",
    }
)

st.dataframe(
    display_forecasts,
    use_container_width=True,
    hide_index=True,
)


# Model monitoring
st.subheader("Model Monitoring")

monitoring_mae = performance["absolute_error"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Test MAE",
    "43.69",
)

col2.metric(
    "Test RMSE",
    "55.08",
)

col3.metric(
    "Monitoring MAE",
    f"{monitoring_mae:.2f}",
)

st.caption(
    "Test metrics are calculated on the held-out November-December test period. "
    "Monitoring MAE is calculated only from saved batch forecasts for which "
    "actual outcomes are available."
)


# Forecast performance
st.write("Forecast Performance")

performance_display = performance[
    [
        "forecast_date",
        "predicted_active_customers",
        "actual_active_customers",
        "absolute_error",
    ]
].copy()

performance_display["forecast_date"] = (
    performance_display["forecast_date"].dt.strftime("%Y-%m-%d")
)

performance_display = performance_display.rename(
    columns={
        "forecast_date": "Forecast Date",
        "predicted_active_customers": "Predicted Active Customers",
        "actual_active_customers": "Actual Active Customers",
        "absolute_error": "Absolute Error",
    }
)

st.dataframe(
    performance_display,
    use_container_width=True,
    hide_index=True,
)


# Data drift
st.write("Data Drift")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Features Monitored",
    "13",
)

col2.metric(
    "Features with Drift",
    "2",
)

col3.metric(
    "Drift Share",
    "15.4%",
)

st.write(
    "Evidently detected feature drift in **month** and "
    "**dac_rolling_mean_14** during the simulated production period."
)

st.caption(
    "The month feature is expected to differ because the reference and "
    "monitoring periods cover different calendar months. Drift is treated "
    "as a signal for investigation rather than an automatic trigger for "
    "model replacement."
)