import streamlit as st
import pandas as pd
import joblib
import os
import gdown
model_path = "crop_yield_model.pkl"
model = joblib.load(model_path)

# =========================
# App configuration
# =========================

st.set_page_config(
    page_title="Crop Yield Prediction",
    page_icon="🌾",
    layout="centered"
)

st.title("🌾 Crop Yield Prediction Dashboard")

st.write(
    "Enter the agricultural and environmental parameters "
    "to predict crop yield."
)


# =========================
# Load dataset for dropdowns
# =========================

CSV_FILE = "crop_yield.csv"

if os.path.exists(CSV_FILE):

    df = pd.read_csv(CSV_FILE)

    if df.columns[0].startswith("Unnamed"):
        df = df.drop(columns=[df.columns[0]])

    df.columns = df.columns.str.strip()

    areas = sorted(df["Area"].dropna().unique())
    crops = sorted(df["Item"].dropna().unique())

else:
    st.error("CSV dataset was not found.")
    st.stop()


# =========================
# User inputs
# =========================

st.subheader("🌱 Farm Information")

area = st.selectbox(
    "📍 Area",
    areas
)

crop = st.selectbox(
    "🌾 Crop",
    crops
)

year = st.number_input(
    "📅 Year",
    min_value=1990,
    max_value=2035,
    value=2025,
    step=1
)


st.subheader("🌦️ Environmental Conditions")

rainfall = st.number_input(
    "🌧️ Average Rainfall (mm/year)",
    min_value=0.0,
    max_value=5000.0,
    value=1000.0,
    step=10.0
)

pesticides = st.number_input(
    "🧪 Pesticides Used (tonnes)",
    min_value=0.0,
    max_value=10000.0,
    value=100.0,
    step=1.0
)

temperature = st.number_input(
    "🌡️ Average Temperature (°C)",
    min_value=-10.0,
    max_value=50.0,
    value=20.0,
    step=0.1
)


# =========================
# Prediction
# =========================

if st.button("🌾 Predict Yield", type="primary"):

    input_data = pd.DataFrame({
        "Area": [area],
        "Item": [crop],
        "Year": [year],
        "average_rain_fall_mm_per_year": [rainfall],
        "pesticides_tonnes": [pesticides],
        "avg_temp": [temperature]
    })

    try:

        prediction_hg_ha = model.predict(input_data)[0]

        prediction_kg_ha = prediction_hg_ha / 10

        prediction_kg_acre = prediction_kg_ha / 2.47105

        st.success(
            f"🌾 Predicted Crop Yield: "
            f"{prediction_hg_ha:,.2f} hg/ha"
        )

        st.info(
            f"Equivalent to approximately "
            f"{prediction_kg_ha:,.2f} kg/ha "
            f"or {prediction_kg_acre:,.2f} kg/acre."
        )

    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )
