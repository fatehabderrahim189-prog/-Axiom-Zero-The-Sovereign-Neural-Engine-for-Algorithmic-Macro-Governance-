import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Axiom-Zero", layout="wide")

st.title("Axiom-Zero: Economic KPI Forecasting Dashboard")
st.subheader("A student project comparing linear and non-linear forecasting models")
st.write(
    "This dashboard loads a time-indexed economic KPI series, trains two candidate "
    "forecasting models (Linear Regression and Random Forest), evaluates both on a held-out "
    "test split, and reports which one actually performs better on this data — rather than "
    "assuming a more complex model is automatically superior."
)

try:
    data = pd.read_csv("data.csv")

    if "Economic KPI" not in data.columns:
        st.error("data.csv must contain a column named 'Economic KPI'.")
        st.stop()

    x = np.arange(len(data)).reshape(-1, 1)
    y = data["Economic KPI"].values

    # Held-out test split (chronological, not shuffled — this is time-series data)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, shuffle=False
    )

    # Candidate 1: Linear Regression
    lin_model = LinearRegression()
    lin_model.fit(x_train, y_train)
    lin_pred_test = lin_model.predict(x_test)
    lin_mae = mean_absolute_error(y_test, lin_pred_test)
    lin_r2 = r2_score(y_test, lin_pred_test)

    # Candidate 2: Random Forest (genuinely non-linear)
    rf_model = RandomForestRegressor(n_estimators=200, max_depth=4, random_state=42)
    rf_model.fit(x_train, y_train)
    rf_pred_test = rf_model.predict(x_test)
    rf_mae = mean_absolute_error(y_test, rf_pred_test)
    rf_r2 = r2_score(y_test, rf_pred_test)

    st.success("Both models trained and evaluated on a held-out test split.")

    st.subheader("Historical Data")
    st.line_chart(data["Economic KPI"])

    st.subheader("Model Comparison (held-out test performance)")
    comparison = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest"],
        "MAE (lower is better)": [round(lin_mae, 3), round(rf_mae, 3)],
        "R\u00b2 (higher is better)": [round(lin_r2, 3), round(rf_r2, 3)],
    })
    st.table(comparison)

    best_model_name = "Linear Regression" if lin_r2 >= rf_r2 else "Random Forest"
    best_model = lin_model if lin_r2 >= rf_r2 else rf_model
    st.info(
        f"**{best_model_name}** performed better on this held-out test split "
        f"(R\u00b2 = {max(lin_r2, rf_r2):.3f}) and is used for the forecast below."
    )
    if best_model_name == "Linear Regression" and rf_r2 < 0:
        st.caption(
            "Note: Random Forest underperformed here because tree-based models cannot "
            "extrapolate beyond the range of values they were trained on — a well-known "
            "limitation for trend-following time series like this one. This is expected "
            "behavior, not a bug, and is exactly why both models are compared explicitly "
            "rather than assuming the more complex one is automatically better."
        )

    # Refit the chosen model on the full dataset for the actual forward forecast
    best_model.fit(x, y)
    future_x = np.arange(len(data), len(data) + 5).reshape(-1, 1)
    predictions = best_model.predict(future_x)

    st.subheader(f"5-Step Forward Forecast (using {best_model_name})")
    forecast_df = pd.DataFrame({
        "Step": [f"t+{i+1}" for i in range(5)],
        "Predicted Economic KPI": np.round(predictions, 2),
    }).set_index("Step")
    st.line_chart(forecast_df)
    st.table(forecast_df)

except FileNotFoundError:
    st.error("data.csv not found. Please add a CSV file with an 'Economic KPI' column.")
except Exception as e:
    st.error(f"Error: {e}")
    
