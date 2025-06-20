# app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor

# Load dataset and train model (normally you'd load a saved model)
@st.cache_resource
def load_model():
    df = pd.read_csv("yield_df.csv")
    df_maize = df[df["Item"] == "Maize"].drop(columns=["Unnamed: 0", "Item"])
    X = df_maize[['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']]
    y = df_maize['hg/ha_yield']
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = load_model()

# Title
st.title("🌽 Maize Yield Predictor (SDG 2: Zero Hunger)")
st.markdown("Enter environmental conditions to predict **maize crop yield (tons/hectare)**.")

# Input features
rain = st.number_input("Average Rainfall (mm/year)", min_value=0.0, max_value=5000.0, value=1000.0)
pest = st.number_input("Pesticide Use (tonnes)", min_value=0.0, max_value=1000.0, value=100.0)
temp = st.number_input("Average Temperature (°C)", min_value=-10.0, max_value=50.0, value=20.0)

# Predict button
if st.button("Predict Yield"):
    input_data = np.array([[rain, pest, temp]])
    pred = model.predict(input_data)[0]  # in hg/ha
    tons_per_hectare = pred / 10000  # Convert to tons/ha
    st.success(f"📈 Predicted Yield: **{tons_per_hectare:.2f} tons/hectare**")

# Show feature importance
if st.checkbox("Show Feature Importance"):
    features = ['Rainfall', 'Pesticide Use', 'Temperature']
    importances = model.feature_importances_
    df_imp = pd.DataFrame({'Feature': features, 'Importance': importances})
    st.bar_chart(df_imp.set_index('Feature'))
