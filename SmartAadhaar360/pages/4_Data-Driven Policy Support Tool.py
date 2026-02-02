import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Data-Driven Policy Support Tool",
    layout="wide"
)

st.title("🏛️ Data-Driven Policy Support Tool")
st.write(
    "This tool helps policymakers identify **priority districts** "
    "for Aadhaar infrastructure and biometric service planning."
)

# ===============================
# LOAD MODEL & SCALER
# ===============================
model = joblib.load("models/policy_kmeans_model.pkl")
scaler = joblib.load("models/policy_scaler.pkl")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("datasets/biometric_demographic_merge.xls")

features = [
    "bio_age_5_17",
    "bio_age_17_",
    "total_population",
    "age_group_population"
]

df = df.dropna(subset=features)

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.header("🔍 Select Location")

state = st.sidebar.selectbox(
    "Select State",
    sorted(df["state"].unique())
)

state_df = df[df["state"] == state]

district = st.sidebar.selectbox(
    "Select District",
    sorted(state_df["district"].unique())
)

selected_row = state_df[state_df["district"] == district].iloc[0]

# ===============================
# DISTRICT SUMMARY
# ===============================
st.subheader("📊 District Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Biometric (Age 5–17)", int(selected_row["bio_age_5_17"]))
c2.metric("Biometric (Age 17+)", int(selected_row["bio_age_17_"]))
c3.metric("Total Population", int(selected_row["total_population"]))
c4.metric("Age Group Population", int(selected_row["age_group_population"]))

# ===============================
# POLICY PRIORITY PREDICTION
# ===============================
input_data = [[
    selected_row["bio_age_5_17"],
    selected_row["bio_age_17_"],
    selected_row["total_population"],
    selected_row["age_group_population"]
]]

scaled_input = scaler.transform(input_data)
cluster = model.predict(scaled_input)[0]

priority_labels = {
    0: "🟢 Low Priority",
    1: "🟡 Medium Priority",
    2: "🔴 High Priority"
}

st.subheader("📌 Policy Priority Level")
st.success(priority_labels[cluster])

# ===============================
# POLICY RECOMMENDATION
# ===============================
st.subheader("📝 Recommended Policy Action")

if cluster == 2:
    st.error(
        """
        **Immediate Action Required**
        - Deploy mobile Aadhaar enrollment units
        - Increase biometric operators & devices
        - Conduct school & rural enrollment drives
        """
    )
elif cluster == 1:
    st.warning(
        """
        **Moderate Policy Attention Needed**
        - Improve existing Aadhaar centers
        - Awareness campaigns for enrollment
        """
    )
else:
    st.info(
        """
        **Infrastructure Sufficient**
        - Continue monitoring demand
        - Maintain current service capacity
        """
    )

# ===============================
# STATE-LEVEL DISTRIBUTION
# ===============================
st.subheader("📈 State-Level Policy Priority Distribution (%)")

X_state = state_df[features]
X_state_scaled = scaler.transform(X_state)
state_clusters = model.predict(X_state_scaled)

priority_percent = (
    pd.Series(state_clusters)
    .value_counts(normalize=True)
    .mul(100)
)

labels = ["Low Priority", "Medium Priority", "High Priority"]
values = [
    priority_percent.get(0, 0),
    priority_percent.get(1, 0),
    priority_percent.get(2, 0)
]

fig, ax = plt.subplots()
ax.bar(labels, values)
ax.set_ylabel("Percentage (%)")
ax.set_title(f"Policy Priority Distribution in {state}")

st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    "📌 **Project:** Aadhaar Demand Forecasting & Data-Driven Policy Support System  \n"
    "👩‍💻 Powered by UIDAI Biometric & Demographic Analytics"
)
