import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart Infrastructure Planning",
    layout="wide"
)

st.title("🏗️ Smart Infrastructure Planning Recommendation Engine")
st.write(
    "This tool recommends **infrastructure priorities** for Aadhaar/biometric services "
    "based on district-level biometric activity and enrollments."
)

# ===============================
# LOAD MODEL & SCALER
# ===============================
kmeans = joblib.load("models/infra_kmeans_model.pkl")
scaler = joblib.load("models/infra_scaler.pkl")

# ===============================
# LOAD DATASET
# ===============================
df = pd.read_csv("datasets/biometric_enrolment_merge.xls")  # Replace with your CSV file
features = ["bio_age_5_17", "bio_age_17_", "enrolment_count"]
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

c1, c2, c3 = st.columns(3)
c1.metric("Biometric (Age 5–17)", int(selected_row["bio_age_5_17"]))
c2.metric("Biometric (Age 17+)", int(selected_row["bio_age_17_"]))
c3.metric("Enrollment Count", int(selected_row["enrolment_count"]))

# ===============================
# PREDICT PRIORITY
# ===============================
input_data = [[
    selected_row["bio_age_5_17"],
    selected_row["bio_age_17_"],
    selected_row["enrolment_count"]
]]

scaled_input = scaler.transform(input_data)
cluster = kmeans.predict(scaled_input)[0]

# Determine low, medium, high clusters based on mean enrollment
cluster_means = df.groupby('cluster')['enrolment_count'].mean() if 'cluster' in df.columns else pd.Series([0,0,0], index=[0,1,2])
low_cluster = cluster_means.idxmin()
high_cluster = cluster_means.idxmax()
medium_cluster = list(set([0,1,2]) - {low_cluster, high_cluster})[0]

def label_cluster(c):
    if c == low_cluster:
        return "🟢 Low Priority"
    elif c == high_cluster:
        return "🔴 High Priority"
    else:
        return "🟡 Medium Priority"

priority_label = label_cluster(cluster)

st.subheader("📌 Infrastructure Priority Level")
st.success(priority_label)

# ===============================
# RECOMMENDED ACTION
# ===============================
st.subheader("📝 Recommended Policy Action")

if priority_label == "🔴 High Priority":
    st.error(
        """
        **Immediate Action Required**
        - Deploy additional enrollment centers / mobile units
        - Increase operators and devices
        - Conduct awareness campaigns in schools and rural areas
        """
    )
elif priority_label == "🟡 Medium Priority":
    st.warning(
        """
        **Moderate Policy Attention Needed**
        - Optimize existing enrollment centers
        - Plan for expansion in near future
        """
    )
else:
    st.info(
        """
        **Low Priority**
        - Maintain current infrastructure
        - Monitor growth in enrollments
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

labels = ["Low Priority", "Medium Priority", "High Priority"]
values = [
    priority_percent.get(low_cluster, 0),
    priority_percent.get(medium_cluster, 0),
    priority_percent.get(high_cluster, 0)
]

fig, ax = plt.subplots()
ax.bar(labels, values, color=["green", "orange", "red"])
ax.set_ylabel("Percentage (%)")
ax.set_title(f"Policy Priority Distribution in {state}")
st.pyplot(fig)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    "📌 **Project:** Smart Infrastructure Planning Recommendation Engine  \n"
    "👩‍💻 Powered by UIDAI Biometric & Enrollment Data"
)
