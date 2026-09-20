# Daily Active Customer Forecasting

Forecasting daily active banking customers using XGBoost and statistical baselines.

## Project Overview

This project uses a synthetic banking dataset containing approximately one million transactions across 60,000 customers in 2023. The objective is to predict the number of unique customers who will make at least one transaction the following day.

The analysis includes exploratory data analysis, time-series feature engineering, baseline forecasting, XGBoost modelling, feature selection and hyperparameter tuning.

## Key Results

| Model                     | Test MAE (customers) |
| ------------------------- | -------------------: |
| Historical expanding mean |                42.45 |
| Seven-day moving average  |                43.10 |
| XGBoost (tuned)           |                43.63 |
| Naïve forecast            |                58.85 |

Although XGBoost marginally outperformed the expanding mean during validation, this improvement did not persist on the independent test period. The simpler expanding-mean baseline achieved the lowest test MAE, highlighting the importance of comparing machine learning models against straightforward benchmarks.

## Tools and Techniques

Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn and XGBoost.

Techniques include time-series feature engineering, chronological train/validation/test splitting, time-series cross-validation and regression error evaluation.

## Dataset

[Synthetic Global Bank Transactions Dataset — Kaggle](https://www.kaggle.com/datasets/mckenziemakwela/synthetic-global-bank-transactions-dataset)

Download the dataset and place `customers.csv` and `transactions.csv` in the location expected by the notebook. The original dataset is not included in this repository.

## Notebook

[daily_active_customer_forecasting.ipynb](daily_active_customer_forecasting.ipynb)

The notebook contains the complete analysis, model development, visualisations and final evaluation.
