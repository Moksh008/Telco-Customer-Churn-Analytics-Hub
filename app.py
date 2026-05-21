"""
Main entrypoint file for the Telco Customer Churn Analytics portal.
Initializes page properties, loads styles, handles side-navigation routing, 
and invokes modular dashboard views.
"""

import streamlit as st
import warnings

# Suppress sklearn/pandas deprecation or version warnings in production logs
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# 1. Page Configuration Configuration
st.set_page_config(
    page_title="Telco Customer Churn Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modular custom styles, model utilities, and tab views
from src.config import inject_custom_styles, FEATURE_ORDER
from src.utils import load_ml_assets
from src.views.welcome import render_welcome_view
from src.views.single_predictor import render_single_predictor_view
from src.views.batch_predictor import render_batch_predictor_view
from src.views.insights import render_insights_view

# Inject the premium glassmorphic dark theme CSS styles
inject_custom_styles()

# 2. Safe loading of model and scaler binaries with global caching
model, scaler, error_msg = load_ml_assets()

# --- HEADER SECTION ---
col_logo, col_title = st.columns([1, 12])
with col_title:
    st.markdown('<h1 class="hero-title">Telco Customer Churn Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;">Industry-grade Predictive Dashboard powered by scikit-learn & Streamlit</p>', unsafe_allow_html=True)

# Safeguard checkpoint: halts application execution if machine learning pickles are missing
if error_msg:
    st.error(error_msg)
    st.info("Ensure `churn_model.pkl` and `scaler.pkl` exist in the current working directory.")
    st.stop()

# 3. Sidebar Navigation System
st.sidebar.markdown(
    '<div style="text-align: center; padding: 15px 0;"><h2 style="color: #6366F1; font-weight: 800; margin: 0;">⚡ CHURN HUB</h2></div>', 
    unsafe_allow_html=True
)

# Initialize global session navigation variables to support homepage quick-launch button events
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Welcome & Project Overview"

modules_list = [
    "Welcome & Project Overview", 
    "Single Customer Predictor", 
    "Batch CSV Predictor", 
    "Model Global Insights"
]

default_idx = (
    modules_list.index(st.session_state.app_mode) 
    if st.session_state.app_mode in modules_list else 0
)

# Sidebar radio controller
app_mode = st.sidebar.radio(
    "Dashboard Modules", 
    modules_list,
    index=default_idx
)
st.session_state.app_mode = app_mode

st.sidebar.markdown("---")
st.sidebar.markdown("### Model Properties")
st.sidebar.info(
    f"**Algorithm**: RandomForestClassifier\n"
    f"**Features Analyzed**: {len(FEATURE_ORDER)}\n"
    f"**Engine Framework**: Scikit-Learn\n"
    f"**Serialization**: Joblib Binary"
)

# 4. View Router Traffic coordination
if app_mode == "Welcome & Project Overview":
    render_welcome_view()
elif app_mode == "Single Customer Predictor":
    render_single_predictor_view(model, scaler)
elif app_mode == "Batch CSV Predictor":
    render_batch_predictor_view(model, scaler)
elif app_mode == "Model Global Insights":
    render_insights_view(model)

# --- GLOBAL FOOTER ---
st.markdown("""
<div class="footer">
    <p>Churn Hub - Customer Churn Prediction System | Powered by RandomForestClassifier | Version 1.0.0 Pro</p>
</div>
""", unsafe_allow_html=True)
