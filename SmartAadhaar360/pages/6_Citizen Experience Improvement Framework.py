import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Citizen Experience Improvement",
    layout="wide"
)

st.title("👥 Citizen Experience Improvement Framework")
st.write(
    "This tool identifies districts/pincodes where **citizen experience with biometric services** "
    "can be improved based on total biometric updates."
)

# ===============================
# LOAD MODEL & SCALER
# ===============================
kmeans = joblib.load("models/citizen_kmeans_model.pkl")
scaler = joblib.load("models/citizen_scaler.pkl")

# ===============================
# LOAD DATASET
# ===============================
df = pd.read_csv("datasets/2_uidai_biometric.xls")  # Replace with your CSV file
features = ["total_biometric_updates"]
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
    "Select District/Pincode",
    sorted(state_df["district"].unique())
)

selected_row = state_df[state_df["district"] == district].iloc[0]

# ===============================
# DISTRICT OVERVIEW
# ===============================
st.subheader("📊 District Overview")
st.metric("Total Biometric Updates", int(selected_row["total_biometric_updates"]))

# ===============================
# PREDICT PRIORITY
# ===============================
input_data = [[selected_row["total_biometric_updates"]]]
scaled_input = scaler.transform(input_data)
cluster = kmeans.predict(scaled_input)[0]

# Identify clusters
cluster_means = df.groupby('cluster')['total_biometric_updates'].mean() if 'cluster' in df.columns else pd.Series([0,0,0], index=[0,1,2])
low_cluster = cluster_means.idxmin()
high_cluster = cluster_means.idxmax()
medium_cluster = list(set([0,1,2]) - {low_cluster, high_cluster})[0]

def label_cluster(c):
    if c == low_cluster:
        return "🟢 Low Improvement Need"
    elif c == high_cluster:
        return "🔴 High Improvement Need"
    else:
        return "🟡 Medium Improvement Need"

priority_label = label_cluster(cluster)
st.subheader("📌 Citizen Experience Improvement Priority")
st.success(priority_label)

# ===============================
# RECOMMENDED ACTION
# ===============================
st.subheader("📝 Recommended Actions")
if priority_label == "🔴 High Improvement Need":
    st.error(
        """
        - Deploy more counters or mobile units in this district/pincode
        - Increase staff and operational hours
        - Reduce waiting time for citizens
        - Conduct awareness campaigns
        """
    )
elif priority_label == "🟡 Medium Improvement Need":
    st.warning(
        """
        - Optimize existing centers
        - Monitor biometric update trends
        - Plan for future infrastructure scaling
        """
    )
else:
    st.info(
        """
        - Maintain current infrastructure
        - Regular monitoring is sufficient
        """
    )

# ===============================
# STATE-LEVEL DISTRIBUTION
# ===============================
st.subheader("📈 State-Level Priority Distribution (%)")
X_state = state_df[features]
X_state_scaled = scaler.transform(X_state)
state_clusters = kmeans.predict(X_state_scaled)
priority_percent = pd.Series(state_clusters).value_counts(normalize=True).mul(100)

labels = ["Low Improvement Need", "Medium Improvement Need", "High Improvement Need"]
values = [
    priority_percent.get(low_cluster, 0),
    priority_percent.get(medium_cluster, 0),
    priority_percent.get(high_cluster, 0)
]

fig, ax = plt.subplots()
ax.bar(labels, values, color=["green", "orange", "red"])
ax.set_ylabel("Percentage (%)")
ax.set_title(f"Citizen Experience Improvement Distribution in {state}")
st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    "📌 **Project:** Citizen Experience Improvement Framework  \n"
    "👩‍💻 Powered by UIDAI Biometric Update Data"
)
