# Wise Remittance Pricing Analysis

### Competitive Pricing Benchmark | UK Outbound Remittances | 2022–2025

## Project Overview

This independent data analytics project investigates Wise's historical remittance pricing competitiveness across three UK outbound corridors: Bangladesh, Pakistan and Nepal.

Using Python, I analysed historical transfer pricing data, compared Wise's costs against matched competitors, identified pricing anomalies and translated the findings into actionable business recommendations.

**Objective:** Identify where Wise may face competitive pricing pressure and determine which corridors warrant further investigation.

## Tools & Technologies

- **Python:** Pandas, NumPy, Matplotlib
- **Data Analysis:** Exploratory Data Analysis (EDA), data cleaning and aggregation
- **Statistical Methods:** Median-based benchmarking, robust z-score anomaly detection and sensitivity analysis
- **Development:** Jupyter Notebook

## Dataset

**Source:** World Bank — Remittance Prices Worldwide (RPW)

**Period analysed:** 2022–2025

**Scope:** UK outbound remittances to Bangladesh, Pakistan and Nepal.

The original dataset is excluded from this repository due to its size.

## Methodology

### 1. Data Preparation
- Filtered historical remittance pricing observations for UK outbound transfers.
- Standardised relevant fields and examined data quality.
- Selected Bangladesh, Pakistan and Nepal for detailed corridor-level analysis.

### 2. Competitor Benchmarking
- Matched Wise observations against competitors using destination, quarter, payment method and payout method.
- Calculated median competitor transfer costs for each matched group.
- Defined the pricing gap as:

  **Pricing Gap = Wise Total Cost (%) − Median Competitor Total Cost (%)**

### 3. Anomaly Detection
- Applied robust z-score analysis to identify unusually large pricing gaps.
-