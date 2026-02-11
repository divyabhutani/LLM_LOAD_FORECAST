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
1. For each utility, the time series is split into:
   - **History:** all observations except the final 24 hours
   - **Holdout:** the final 24 hours (used exclusively for evaluation)
2. A lightweight open-source language model (`sshleifer/tiny-gpt2`) is used as the primary forecasting model, not merely for preprocessing or formatting.
3. The LLM is prompted with the most recent hourly load values and instructed to directly generate the next 24 hourly load values.
4. Simple post-processing ensures:
 - Exactly 24 numeric forecast values
 - No negative load values

This design keeps the system readable, runnable, and fully reproducible.

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
- Holdout data is used exclusively for evaluation after forecasting
- No future information is leaked into the LLM prompt

---

## Assumptions
- Short-term electricity load behavior is primarily driven by recent historical values
- No external features (e.g., weather or calendar effects) are available
- This is a prototype intended to demonstrate feasibility rather than optimize accuracy

---

## Reproducibility
The project runs entirely locally using an open-source LLM and does not rely on any
external APIs or API keys. The full pipeline is containerized using Docker to ensure
reproducible execution.

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
