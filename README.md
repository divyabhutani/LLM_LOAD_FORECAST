# LLM_LOAD_FORECAST

 LLM-Based Short-Term Utility Load Forecasting 

## Overview
This project implements a prototype short-term electricity load forecaster where a Large Language Model (LLM) is the primary forecasting component.

For each utility company, the system produces hourly point forecasts for the next 24 hours using only historical load data. The goal is to demonstrate a clear, reproducible, and methodologically sound approach to LLM-based time-series forecasting, prioritizing code quality and correctness over raw accuracy.

The full pipeline runs end-to-end without manual intervention and is fully containerized for reproducibility.


## Data
- **Input:** Three CSV files, one per utility company
- **Time span:** Approximately three months of hourly load measurements per utility
- **Schema:** Each utility is processed independently

---

## Forecasting Methodology

For each utility, the following steps are executed:
1. Train / Holdout Split
All but the final 24 hours are used as historical context
The final 24 hours are strictly held out for evaluation
2. LLM-Based Forecasting
A lightweight open-source language model (sshleifer/tiny-gpt2) is used as the primary forecasting model
The model is prompted with recent hourly load values and instructed to directly generate the next 24 hourly load values
The LLM is responsible for producing the numerical forecasts, not merely formatting or preprocessing data
3. Post-Processing
Enforces exactly 24 numeric forecast values
Clips negative values to zero
Ensures outputs are valid and evaluable
This approach intentionally favors simplicity, transparency, and reproducibility.


---

## Out-of-Sample Evaluation
To avoid data leakage, the final 24 hours of each utility’s data are strictly held out and never included in the model input.

The following evaluation metrics are reported:
- **Mean Absolute Error (MAE)**
- **Mean Absolute Percentage Error (MAPE)**
- **Root Mean Squared Error (RMSE)**

---

## Data Leakage Prevention
- Forecast inputs include only historical load values available at prediction time
- Holdout data is never included in the LLM prompt
- Metrics are computed strictly on unseen data
- No future information is leaked into model inputs


---

## Reproducibility
- Forecast inputs include only historical load values available at prediction time
- Holdout data is never included in the LLM prompt
- Metrics are computed strictly on unseen data
- No future information is leaked into model inputs


---

## Project Structure
```
llm-load-forecast/
├── data/
│ ├── utility_1.csv
│ ├── utility_2.csv
│ └── utility_3.csv
├── main.py
├── Dockerfile
└── README.md
```

---

## How to Run
### Local Execution

```
Ensure Python 3 is installed, then run: python3 main.py
```
### Docker Execution
```
docker build -t llm-load-forecast .
docker run llm-load-forecast
```
