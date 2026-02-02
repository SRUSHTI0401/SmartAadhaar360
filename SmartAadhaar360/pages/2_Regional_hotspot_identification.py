import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="UIDAI Regional Hotspot Identification",
    layout="wide"
)

st.title("🔥 UIDAI Biometric Regional Hotspot Identification")

st.write(
    "This module identifies **district-level biometric service hotspots** "
    "using clustering on UIDAI biometric update data."
)

# =========================
# LOAD MODEL & SCALER
# =========================
kmeans = joblib.load("models/hotspot_kmeans_model.pkl")
scaler = joblib.load("models/hotspot_scaler.pkl")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("datasets/2_uidai_biometric.xls")

# =========================
# FEATURE ENGINEERING
# =========================
X = df[['total_biometric_updates']]
X_scaled = scaler.transform(X)

df['cluster'] = kmeans.predict(X_scaled)

# =========================
# CLUSTER INTERPRETATION
# =========================
cluster_means = df.groupby('cluster')['total_biometric_updates'].mean()
low_cluster = cluster_means.idxmin()
high_cluster = cluster_means.idxmax()

def label_cluster(c):
    if c == low_cluster:
        return "Low Demand"
    elif c == high_cluster:
        return "High Demand"
    else:
        return "Medium Demand"

df['hotspot_label'] = df['cluster'].apply(label_cluster)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

state_filter = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df['state'].unique().tolist())
)

demand_filter = st.sidebar.selectbox(
    "Select Demand Type",
    ["All", "High Demand", "Medium Demand", "Low Demand"]
)

# Apply state filter
if state_filter != "All":
    filtered_df = df[df['state'] == state_filter]
else:
    filtered_df = df.copy()

# Apply demand filter
if demand_filter != "All":
    filtered_df = filtered_df[filtered_df['hotspot_label'] == demand_filter]

# =========================
# DATA OUTPUT
# =========================
st.subheader("📊 Filtered Hotspot Data")
st.dataframe(
    filtered_df[['state', 'district', 'pincode', 'total_biometric_updates', 'hotspot_label']]
    .sort_values(by='total_biometric_updates', ascending=False)
)

st.metric(
    label="Number of Districts in Selection",
    value=len(filtered_df)
)

# =========================
# DEMAND DISTRIBUTION CHART
# =========================
st.subheader("📈 Demand Distribution in Selected State")

# Only show chart for selected state
if state_filter != "All":
    dist_counts = df[df['state'] == state_filter]['hotspot_label'].value_counts()
else:
    dist_counts = df['hotspot_label'].value_counts()

# Convert counts to percentage
dist_percent = (dist_counts / dist_counts.sum() * 100).round(2)

st.bar_chart(dist_percent)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "📌 **Project:** Aadhaar Demand Forecasting & Regional Hotspot Identification System  \n"
    "👩‍💻 Developed using UIDAI Biometric Data & Machine Learning"
)
