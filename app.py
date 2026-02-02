# import streamlit as st

# # Main landing page
# st.set_page_config(
#     page_title="SmartAadhaar360",
#     layout="wide"
# )

# st.title("🚀 SmartAadhaar360")
# st.write(
#     """
#     Welcome to **SmartAadhaar360** – a unified platform for Aadhaar-based service optimization.
    
#     Navigate through the sidebar to explore each feature:
#     1. Aadhaar Demand Forecasting System
#     2. Regional Hotspot Identification
#     3. Age-Group Based Biometric Service Optimization
#     4. Data-Driven Policy Support Tool
#     5. Smart Infrastructure Planning Recommendation Engine
#     6. Citizen Experience Improvement Framework
#     """
# )

# # -------------------------------
# # Feature Purposes Section
# # -------------------------------
# st.markdown("---")
# st.subheader("📌 Feature Purposes Overview")

# st.markdown("""
# **1. Aadhaar Demand Forecasting System**  
# Predicts expected Aadhaar biometric service demand at district/state level to help plan resources, staff, and centers efficiently.

# **2. Regional Hotspot Identification**  
# Identifies districts with high/medium/low biometric service activity using clustering to highlight service hotspots.

# **3. Age-Group Based Biometric Service Optimization**  
# Analyzes demand by age group (5–17 & 17+) to optimize service deployment for different demographics.

# **4. Data-Driven Policy Support Tool**  
# Clusters districts based on biometric and demographic data to support policymakers in allocating resources and interventions.

# **5. Smart Infrastructure Planning Recommendation Engine**  
# Provides recommendations for infrastructure development and prioritization at state/district level based on biometric demand trends.

# **6. Citizen Experience Improvement Framework**  
# Enhances user experience by predicting high-demand centers, enabling better queue management and service distribution.
# """)


import streamlit as st

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="SmartAadhaar360",
    layout="wide",
    page_icon="🛠️"
)

# ------------------------
# Hero Banner
# ------------------------
st.markdown(
    """
    <div style='background-color:#1F4E79;padding:30px;border-radius:10px'>
        <h1 style='color:white;text-align:center;font-family:Arial, sans-serif;'>SmartAadhaar360</h1>
        <p style='color:white;text-align:center;font-size:18px;font-family:Arial, sans-serif;'>
            A unified platform for Aadhaar-based service optimization and data-driven decision making.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("")

# ------------------------
# Introduction
# ------------------------
st.markdown("""
Welcome to **SmartAadhaar360**, a professional platform designed to optimize Aadhaar-based services.  
Use the sidebar to navigate to each feature for detailed insights, forecasts, and recommendations.
""")

# ------------------------
# Feature Cards Section
# ------------------------
st.subheader("Feature Overview")

cols = st.columns(3)

feature_list = [
    ("Aadhaar Demand Forecasting", "Forecast biometric service demand at district and state level to plan resources effectively."),
    ("Regional Hotspot Identification", "Identify high, medium, and low demand districts using clustering techniques."),
    ("Age-Group Based Service Optimization", "Optimize service deployment based on demand patterns across age groups."),
    ("Data-Driven Policy Support Tool", "Provide insights to policymakers for resource allocation and intervention planning."),
    ("Smart Infrastructure Planning", "Recommend infrastructure development priorities using demand trends and predictions."),
    ("Citizen Experience Improvement Framework", "Enhance user experience through high-demand predictions and optimized service distribution.")
]

for i, (title, desc) in enumerate(feature_list):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div style='padding:20px;border-radius:10px;background-color:#F0F4F8;box-shadow: 2px 2px 8px #D0D3D4'>
                <h3 style='color:#1F4E79;font-family:Arial, sans-serif;'>{title}</h3>
                <p style='font-size:14px;font-family:Arial, sans-serif;color:#333333;'>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# ------------------------
# Feature Purposes Table
# ------------------------
st.subheader("Detailed Feature Purposes")

st.markdown("""
| Feature | Purpose |
|---------|---------|
| Aadhaar Demand Forecasting | Predicts expected biometric service demand at district/state level to enable efficient resource planning. |
| Regional Hotspot Identification | Identifies districts with high, medium, or low biometric service activity using clustering algorithms. |
| Age-Group Based Biometric Service Optimization | Analyzes demand across age groups to optimize service deployment and resource allocation. |
| Data-Driven Policy Support Tool | Clusters districts based on demographic and biometric data to support evidence-based policymaking. |
| Smart Infrastructure Planning Recommendation Engine | Provides recommendations for infrastructure development based on service demand trends. |
| Citizen Experience Improvement Framework | Enhances user experience by predicting high-demand centers and improving service distribution. |
""")
