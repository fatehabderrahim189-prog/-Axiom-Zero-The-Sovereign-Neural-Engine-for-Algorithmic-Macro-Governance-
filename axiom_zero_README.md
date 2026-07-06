# Axiom-Zero: Economic KPI Forecasting Dashboard

A Streamlit dashboard that forecasts a time-indexed economic KPI series by training and
comparing two candidate models — Linear Regression and Random Forest — and selecting
whichever one actually performs better on held-out data, rather than assuming a more
complex model is automatically superior.

## What this project actually does

1. **Loads** a time-indexed economic KPI series from `data.csv`.
2. **Trains two models** on a chronological train/test split:
   - Linear Regression (a linear trend model)
   - Random Forest Regressor (a genuinely non-linear, tree-based model)
3. **Evaluates both** on held-out test data using MAE and R².
4. **Selects the better-performing model** for the forward forecast, and reports why.

## An honest finding, not a marketing claim

On this dataset (a roughly linear, steadily increasing economic trend), **Linear
Regression outperforms Random Forest**, often substantially. This is expected: tree-based
models like Random Forest cannot extrapolate beyond the range of values seen in training —
for a steadily rising trend, a Random Forest forecast flattens out instead of continuing
the trend, while Linear Regression correctly continues it.

This project is deliberately built to surface that comparison explicitly rather than to
assume "more complex" means "better." Choosing the right model for the data, and being able
to explain why, is the actual point of this project.

## Tech stack

- **Core:** Python
- **Data handling:** Pandas, NumPy
- **Modeling:** Scikit-Learn (LinearRegression, RandomForestRegressor)
- **Frontend:** Streamlit

## Running locally

```bash
pip install streamlit pandas numpy scikit-learn
streamlit run app.py
```

Requires a `data.csv` file in the same directory with a column named `Economic KPI`.

## Honest scope

This is a first-year student portfolio project demonstrating a complete, correct,
honestly-evaluated forecasting pipeline. It is not a production economic forecasting
system, does not use real macroeconomic data sources, and makes no claims about
governance, policy, or national-scale decision-making — it forecasts one numeric time
series and reports, transparently, which of two models does that better.

## Future improvements

- Add more sophisticated time-series models (ARIMA, Prophet) as further candidates in
  the comparison, rather than replacing the current honest comparison.
- Support multiple KPI columns and cross-KPI comparison.
- Add confidence intervals to the forecast rather than point predictions only.
