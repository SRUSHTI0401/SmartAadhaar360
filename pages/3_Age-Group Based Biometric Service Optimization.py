import streamlit as st
import pandas as pd
import joblib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="UIDAI Age-Group Service Optimization",
    layout="wide"
)

st.title("👥 UIDAI Age-Group Based Biometric Service Optimization")

st.write(
    "This module analyzes **age-wise biometric service demand** to help "
    "optimize UIDAI infrastructure at **pincode level**."
)

# =========================
# LOAD MODEL & SCALER
# =========================
kmeans = joblib.load("models/age_group_kmeans_model.pkl")
scaler = joblib.load("models/age_group_scaler.pkl")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("datasets/uidai_biometric.xls")

# =========================
# FEATURE ENGINEERING
# =========================
df['total_biometric_updates'] = df['bio_age_5_17'] + df['bio_age_17_']
df = df[df['total_biometric_updates'] > 0]

df['age_5_17_ratio'] = df['bio_age_5_17'] / df['total_biometric_updates']
df['age_17_plus_ratio'] = df['bio_age_17_'] / df['total_biometric_updates']

X = df[['age_5_17_ratio', 'age_17_plus_ratio']]
X_scaled = scaler.transform(X)

df['cluster'] = kmeans.predict(X_scaled)

# =========================
# CLUSTER INTERPRETATION
# =========================
def label_cluster(row):
    if row['age_5_17_ratio'] > 0.6:
        return "Child-Dominant Demand (5–17)"
    elif row['age_17_plus_ratio'] > 0.6:
        return "Adult-Dominant Demand (17+)"
    else:
        return "Balanced Demand"

df['age_group_category'] = df.apply(label_cluster, axis=1)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

state_filter = st.sidebar.selectbox(
    "Select State",
    sorted(df['state'].unique())
)

district_filter = st.sidebar.selectbox(
    "Select District",
    ["All"] + sorted(
        df[df['state'] == state_filter]['district'].unique()
    )
)

filtered_df = df[df['state'] == state_filter]

if district_filter != "All":
    filtered_df = filtered_df[filtered_df['district'] == district_filter]

# =========================
# OUTPUT TABLE
# =========================
st.subheader("📊 Age-Group Demand Analysis")

st.dataframe(
    filtered_df[
        ['state', 'district', 'pincode',
         'bio_age_5_17', 'bio_age_17_',
         'age_group_category']
    ]
)

st.metric(
    label="Number of Pincodes Analyzed",
    value=len(filtered_df)
)

# =========================
# PERCENTAGE VISUALIZATION
# =========================
st.subheader("📈 Age-Group Demand Distribution (%)")

age_counts = filtered_df['age_group_category'].value_counts()
age_percent = (age_counts / age_counts.sum() * 100).round(2)

st.bar_chart(age_percent)

# =========================
# SERVICE INSIGHTS
# =========================
st.subheader("🛠 Service Optimization Insights")

def recommendation(category):
    if "Child" in category:
        return "Deploy school-based enrollment camps & child biometric kits"
    elif "Adult" in category:
        return "Increase adult service counters & working-hour availability"
    else:
        return "Maintain balanced staffing & infrastructure"

filtered_df['service_recommendation'] = filtered_df['age_group_category'].apply(recommendation)

st.dataframe(
    filtered_df[
        ['pincode', 'age_group_category', 'service_recommendation']
    ]
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "📌 **Feature 3:** Age-Group Based Service Optimization  \n"
    "👩‍💻 ML Model: K-Means Clustering on Age-Wise Biometric Demand"
)
