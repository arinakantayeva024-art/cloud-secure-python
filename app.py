import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import gdown  

# Google Drive file ID (Replace with your actual file ID)
file_id = "1a7paF89c9I5ChaL4SCW_vNlIPAWU6bZl"  # Update with your actual file ID
model_path = "crop_yield_model.pkl"

# Download model if not already available
if not os.path.exists(model_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, model_path, quiet=False)

# Load the trained model
model = joblib.load(model_path)

# Model performance stats (replace with actual values if available)
MODEL_R2 = 0.87  # Example R² score
MODEL_ACC = 0.82  # Example accuracy

# Streamlit UI
st.title("🌾 Crop Yield Prediction Dashboard")
st.write("Enter the farm details below to predict crop yield.")

# Show model performance
with st.expander("ℹ️ Model Performance"):
    st.write(f"**R² Score:** {MODEL_R2}")
    st.write(f"**Accuracy:** {MODEL_ACC}")

# User inputs with realistic ranges and zero as default
temperature = st.number_input(
    "🌡️ Average Temperature (°C)", min_value=10.0, max_value=45.0, step=0.1, value=10.0,
    help="Recommended: 10–45°C"
)
rainfall = st.number_input(
    "🌧️ Rainfall (mm/year)", min_value=200.0, max_value=1200.0, step=10.0, value=200.0,
    help="Recommended: 200–1200 mm/year"
)
pesticides = st.number_input(
    "🧪 Pesticides Used (tonnes)", min_value=0.0, max_value=1000.0, step=0.1, value=0.0
)
soil_type = st.selectbox("🌱 Soil Type", ["Sandy", "Loamy", "Clay", "Silt"])

# Additional Inputs
nitrogen = st.number_input(
    "💨 Nitrogen Content (%)", min_value=0.0, max_value=100.0, step=0.1, value=0.0
)
phosphorus = st.number_input(
    "🧪 Phosphorus Content (%)", min_value=0.0, max_value=100.0, step=0.1, value=0.0
)
potassium = st.number_input(
    "🧂 Potassium Content (%)", min_value=0.0, max_value=100.0, step=0.1, value=0.0
)

# Only enable Predict button if all required fields are in valid range
inputs_valid = (
    10 <= temperature <= 45 and
    200 <= rainfall <= 1200 and
    0 <= pesticides <= 1000 and
    0 <= nitrogen <= 100 and
    0 <= phosphorus <= 100 and
    0 <= potassium <= 100
)

if not inputs_valid:
    st.warning("Please enter all values within their realistic ranges to enable prediction.")

# Soil type encoding (label encoding; ensure your model was trained this way)
soil_types = {"Sandy": 0, "Loamy": 1, "Clay": 2, "Silt": 3}
soil_type_value = soil_types[soil_type]

# Predict button (disabled if inputs are invalid)
if st.button("Predict Yield", disabled=not inputs_valid):
    # Prepare input data
    input_data = np.array([[temperature, rainfall, pesticides, soil_type_value, nitrogen, phosphorus, potassium]])
    prediction_hg_ha = model.predict(input_data)[0]  # Output in hg/ha

    # Convert hg/ha to kg/acre
    prediction_kg_acre = (prediction_hg_ha * 0.1) / 2.47105

    st.success(f"🌾 Predicted Crop Yield: {round(prediction_kg_acre, 2)} kg/acre")
    st.caption("Rainfall is expected in mm/year. Please verify your inputs.")
