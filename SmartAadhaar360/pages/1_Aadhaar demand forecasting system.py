import streamlit as st
import numpy as np
import joblib
from datetime import datetime

# ---------------- Load ML Pipeline ----------------
data = joblib.load("models/aadhaar_demand_forecasting_pipeline.pkl")

model = data['model']
le_state = data['state_encoder']
le_district = data['district_encoder']

# ---------------- Streamlit Page Config ----------------
st.set_page_config(
    page_title="Aadhaar Demand Forecasting",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Aadhaar Demand Forecasting System")
st.markdown(
    "Predict future Aadhaar biometric service demand using historical biometric "
    "and enrolment data."
)

st.divider()

# ---------------- Inputs ----------------

# 📅 Calendar picker
selected_date = st.date_input(
    "📅 Select Month",
    value=datetime(2025, 3, 1)
)

month = selected_date.month
year = selected_date.year

state = st.selectbox("🏛️ State", le_state.classes_)
district = st.selectbox("📍 District", le_district.classes_)

pincode = st.number_input(
    "📮 Pincode",
    min_value=100000,
    max_value=999999
)

bio_5_17 = st.number_input(
    "Biometric Updates (Age 5–17)",
    min_value=0
)

bio_17_plus = st.number_input(
    "Biometric Updates (Age 17+)",
    min_value=0
)

enrolment_count = st.number_input(
    "New Enrolments",
    min_value=0
)

# ---------------- Prediction ----------------
if st.button("🔮 Predict Aadhaar Demand"):
    try:
        state_encoded = le_state.transform([state])[0]
        district_encoded = le_district.transform([district])[0]

        X = np.array([[
            state_encoded,
            district_encoded,
            pincode,
            bio_5_17,
            bio_17_plus,
            enrolment_count,
            month,
            year
        ]])

        prediction = model.predict(X)[0]

        st.success(
            f"📈 **Expected Aadhaar Service Demand:** {int(prediction)}"
        )

    except Exception as e:
        st.error(f"Prediction error: {e}")

st.divider()
st.caption("UIDAI Decision Support System | ML-based Forecasting")
