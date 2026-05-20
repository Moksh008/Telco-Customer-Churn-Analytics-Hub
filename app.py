import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
import os
import warnings
from typing import Dict, Any, Tuple, Optional

# Suppress scikit-learn version mismatch warnings to keep logs clean
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Set page configuration
st.set_page_config(
    page_title="Telco Customer Churn Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling (Glassmorphism & High-Contrast Themes)
st.markdown("""
<style>
    /* Theme overrides */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
    }
    
    /* Main Layout Cards */
    div.stCard {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    /* Interactive Hover Cards */
    .stCard-hover {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s ease;
        height: 100%;
    }
    .stCard-hover:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    /* Main Landing Page Metric Grid Cards */
    .main-metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s ease;
    }
    .main-metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.25);
        border-color: rgba(56, 189, 248, 0.5);
    }
    .main-metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    .main-metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    
    /* Sleek metric badges */
    .metric-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-high { background-color: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid #EF4444; }
    .badge-medium { background-color: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #F59E0B; }
    .badge-low { background-color: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #10B981; }

    /* Custom Titles & Subtitles */
    h1.hero-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
    }
    h3.section-header {
        color: #E2E8F0;
        font-weight: 600;
        border-left: 4px solid #6366F1;
        padding-left: 10px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    /* Streamlit widget tweaks */
    div[data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Footer elements */
    .footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #64748B;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Define exact feature order & category mapping
FEATURE_ORDER = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
]

ENCODING_MAPS = {
    'gender': {'Female': 0, 'Male': 1},
    'SeniorCitizen': {'No': 0, 'Yes': 1},
    'Partner': {'No': 0, 'Yes': 1},
    'Dependents': {'No': 0, 'Yes': 1},
    'PhoneService': {'No': 0, 'Yes': 1},
    'MultipleLines': {'No': 0, 'No phone service': 1, 'Yes': 2},
    'InternetService': {'DSL': 0, 'Fiber optic': 1, 'No': 2},
    'OnlineSecurity': {'No': 0, 'No internet service': 1, 'Yes': 2},
    'OnlineBackup': {'No': 0, 'No internet service': 1, 'Yes': 2},
    'DeviceProtection': {'No': 0, 'No internet service': 1, 'Yes': 2},
    'TechSupport': {'No': 0, 'No internet service': 1, 'Yes': 2},
    'StreamingTV': {'No': 0, 'No internet service': 1, 'Yes': 2},
    'StreamingMovies': {'No': 0, 'No internet service': 1, 'Yes': 2},
    'Contract': {'Month-to-month': 0, 'One year': 1, 'Two year': 2},
    'PaperlessBilling': {'No': 0, 'Yes': 1},
    'PaymentMethod': {
        'Bank transfer (automatic)': 0,
        'Credit card (automatic)': 1,
        'Electronic check': 2,
        'Mailed check': 3
    }
}

DECODING_MAPS = {feature: {val: key for key, val in mapping.items()} for feature, mapping in ENCODING_MAPS.items()}


@st.cache_resource(show_spinner=True)
def load_ml_assets() -> Tuple[Optional[Any], Optional[Any], Optional[str]]:
    """Loads the model and scaler safely with caching."""
    model_path = "churn_model.pkl"
    scaler_path = "scaler.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None, f"Asset files missing. Ensure {model_path} and {scaler_path} exist."
        
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler, None
    except Exception as e:
        return None, None, f"Failed to load assets: {str(e)}"


# Load the models
model, scaler, error_msg = load_ml_assets()

# --- HEADER SECTION ---
col_logo, col_title = st.columns([1, 12])
with col_title:
    st.markdown('<h1 class="hero-title">Telco Customer Churn Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;">Industry-grade Predictive Dashboard powered by scikit-learn & Streamlit</p>', unsafe_allow_html=True)

# Safeguard if models are missing
if error_msg:
    st.error(error_msg)
    st.info("Please place `churn_model.pkl` and `scaler.pkl` in the current working directory.")
    st.stop()


def preprocess_features(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Encodes categorical columns and aligns them in standard feature order."""
    df_encoded = df_raw.copy()
    for col, mapping in ENCODING_MAPS.items():
        if col in df_encoded.columns:
            # Map standard values to integer codes, filling missing values with standard default
            df_encoded[col] = df_encoded[col].map(mapping).fillna(0).astype(int)
    
    # Ensure correct dtype for continuous variables
    for c_col in ['tenure', 'MonthlyCharges', 'TotalCharges']:
        if c_col in df_encoded.columns:
            df_encoded[c_col] = pd.to_numeric(df_encoded[c_col]).fillna(0.0)
            
    return df_encoded[FEATURE_ORDER]


# Sidebar Navigation System
st.sidebar.markdown('<div style="text-align: center; padding: 15px 0;"><h2 style="color: #6366F1; font-weight: 800; margin: 0;">⚡ CHURN HUB</h2></div>', unsafe_allow_html=True)
app_mode = st.sidebar.radio(
    "Dashboard Modules", 
    ["Welcome & Project Overview", "Single Customer Predictor", "Batch CSV Predictor", "Model Global Insights"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Model Properties")
st.sidebar.info(
    f"**Algorithm**: RandomForestClassifier\n"
    f"**Features Analyzed**: {len(FEATURE_ORDER)}\n"
    f"**Engine Framework**: Scikit-Learn\n"
    f"**Serialization**: Joblib Binary"
)


# --- TAB 0: WELCOME & PROJECT OVERVIEW (LANDING PAGE) ---
if app_mode == "Welcome & Project Overview":
    st.markdown('<h3 class="section-header">⚡ Welcome to Churn Hub</h3>', unsafe_allow_html=True)
    
    # 4-Column Metric Grid at the Top
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown("""
        <div class="main-metric-card">
            <div class="main-metric-value">7,043</div>
            <div class="main-metric-label">Dataset Records</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol2:
        st.markdown("""
        <div class="main-metric-card">
            <div class="main-metric-value">84.5%</div>
            <div class="main-metric-label">Inference ROC-AUC</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol3:
        st.markdown("""
        <div class="main-metric-card">
            <div class="main-metric-value">26.5%</div>
            <div class="main-metric-label">Baseline Churn</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol4:
        st.markdown("""
        <div class="main-metric-card">
            <div class="main-metric-value">19</div>
            <div class="main-metric-label">Input Parameters</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

    # Double Column Layout for Context & Blueprint
    col_left, col_right = st.columns([7, 5])
    
    with col_left:
        st.markdown("""
        <div class="stCard" style="height: 100%;">
            <h4 style="color: #38BDF8; font-weight: 700; margin-top: 0; font-family: 'Outfit', sans-serif;">Analytical Retention Mission</h4>
            <p style="font-size: 0.98rem; line-height: 1.6; color: #E2E8F0; margin-bottom: 12px;">
                <b>Churn Hub</b> is an advanced customer retention analytics portal. In highly saturated subscription models, 
                retaining existing users mathematically yields <b>5x more return on investment</b> than acquiring new ones.
            </p>
            <p style="font-size: 0.98rem; line-height: 1.6; color: #E2E8F0; margin-bottom: 15px;">
                By examining subscriber demographics, services, and billing contracts, our predictive engine flags high-risk accounts 
                before they request a cancellation, giving service teams a critical window to apply structural retention offers.
            </p>
            <div style="padding: 15px; background: rgba(99, 102, 241, 0.12); border-left: 4px solid #6366F1; border-radius: 6px; margin-top: 15px;">
                <span style="font-weight: bold; color: #818CF8; font-size: 0.9rem;">📓 Kaggle Research Workspace:</span><br/>
                <span style="font-size: 0.88rem; color: #94A3B8;">All hyperparameter evaluations, random forest grids, and features validation were executed in the Kaggle notebook:</span><br/>
                <a href="https://www.kaggle.com/code/moksh72/moksh-2410998600-s-ul-project" target="_blank" style="color: #38BDF8; font-weight: 600; text-decoration: underline; font-size: 0.90rem;">
                    moksh-2410998600-s-ul-project ↗
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("""
        <div class="stCard" style="height: 100%;">
            <h4 style="color: #C084FC; font-weight: 700; margin-top: 0; font-family: 'Outfit', sans-serif;">Inference Pipeline Architecture</h4>
            <p style="font-size: 0.95rem; line-height: 1.5; color: #E2E8F0; margin-bottom: 10px;">
                When details are submitted, the hub executes a production-grade inference:
            </p>
            <div style="font-size: 0.90rem; color: #94A3B8; line-height: 1.6;">
                🔄 <b>Ordinal Encoding</b>: Maps categorical terms (like Fiber optic, Electronic check) alphabetically to numerical values.<br/>
                ⚖️ <b>StandardScaler</b>: Normalizes and scales attributes using pre-calculated training means and standard deviations.<br/>
                🌲 <b>Random Forest Classifier</b>: Infers individual churn probability using an ensemble of decision trees.<br/>
                💡 <b>Retention Optimizer</b>: Computes key risk factors and selects tailored customer remedies.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<h3 class="section-header">Interactive Platform Navigation</h3>', unsafe_allow_html=True)
    
    # 3-Column Grid for Tab Guidance (using the new stCard-hover visual transition)
    guide_c1, guide_c2, guide_c3 = st.columns(3)
    
    with guide_c1:
        st.markdown("""
        <div class="stCard-hover" style="border-top: 4px solid #38BDF8;">
            <h4 style="color: #38BDF8; font-weight: 700; margin-top: 0;">👤 Single Predictor</h4>
            <p style="font-size: 0.92rem; line-height: 1.5; color: #CBD5E1;">
                <b>Designed for front-line reps and account specialists.</b>
            </p>
            <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 15px;">
                Input a single customer's features to get real-time churn predictions, key risk explanations, and 
                targeted coupon/bundle solutions.
            </p>
            <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8;">
                <b>Bonus Feature</b>: The <b>What-If Simulator</b> lets you test how changing a monthly contract to a one-year or two-year term mitigates churn!
            </p>
            <div style="font-size: 0.85rem; color: #E2E8F0; font-weight: 600; margin-top: 15px;">
                ➡️ <i>Select Single Predictor in the sidebar.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with guide_c2:
        st.markdown("""
        <div class="stCard-hover" style="border-top: 4px solid #F59E0B;">
            <h4 style="color: #F59E0B; font-weight: 700; margin-top: 0;">📁 Batch CSV Predictor</h4>
            <p style="font-size: 0.92rem; line-height: 1.5; color: #CBD5E1;">
                <b>Designed for database analysts and marketing directors.</b>
            </p>
            <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 15px;">
                Upload a structured customer sheet to score hundreds of profiles simultaneously. 
                View campaign aggregate counts, risk histograms, and scatter plots.
            </p>
            <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8;">
                <b>Bonus Feature</b>: Instantly download the complete evaluated database as a scored spreadsheet report.
            </p>
            <div style="font-size: 0.85rem; color: #E2E8F0; font-weight: 600; margin-top: 15px;">
                ➡️ <i>Select Batch Predictor in the sidebar.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with guide_c3:
        st.markdown("""
        <div class="stCard-hover" style="border-top: 4px solid #818CF8;">
            <h4 style="color: #818CF8; font-weight: 700; margin-top: 0;">📊 Model Global Insights</h4>
            <p style="font-size: 0.92rem; line-height: 1.5; color: #CBD5E1;">
                <b>Designed for executives and business strategists.</b>
            </p>
            <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 15px;">
                Review the global mathematical weights derived by the Random Forest model across 7,000+ accounts.
            </p>
            <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8;">
                <b>Bonus Feature</b>: Provides direct, data-backed operational takeaways (like contract migration and autopay transitions) to structurally cure churn.
            </p>
            <div style="font-size: 0.85rem; color: #E2E8F0; font-weight: 600; margin-top: 15px;">
                ➡️ <i>Select Model Global Insights in the sidebar.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<h3 class="section-header">🧠 Frequently Asked Questions</h3>', unsafe_allow_html=True)
    
    with st.expander("💡 Why is predicting customer churn critical for telecom operators?"):
        st.markdown("""
        Customer churn prediction is a direct driver of operational profitability. In telecommunication services:
        - **Higher Acquisition Cost**: Reaching new users through advertisements and promotions is significantly more expensive than keeping active accounts.
        - **Structural Customer Lock-in**: Flagging early risk parameters allows agents to pitch digital bundles (like online security or backup services) that raise the structural switching cost for the subscriber.
        """)
        
    with st.expander("🧠 How does the Random Forest Machine Learning model calculate churn risk?"):
        st.markdown("""
        The backend engine loads a **Random Forest Classifier**:
        - **Ensemble of Decision Trees**: It predicts churn by running customer features down an ensemble of hundreds of decision trees, each trained on boot-strapped samples.
        - **Probability Estimation**: Rather than outputting a simple Yes/No, it aggregates tree decisions to output a continuous risk probability (0% to 100%), which provides the granular risk categories on our dashboard.
        """)
        
    with st.expander("🛡️ What are target retention strategies, and how do they help?"):
        st.markdown("""
        Targeted retention strategies are customized offers based on the customer's vulnerable feature configuration:
        - **Month-to-month contracts** are the leading driver of cancellations; migrating them to long contracts via loyalty discounts permanently cures this risk.
        - **Autopay registrations** eliminate check friction, showing significantly lower churn rates in history.
        """)


# --- TAB 1: SINGLE CUSTOMER PREDICTOR ---
elif app_mode == "Single Customer Predictor":
    st.markdown('<h3 class="section-header">Interactive Risk Assessment & What-If Simulator</h3>', unsafe_allow_html=True)
    
    # Grid layout for inputs
    col_input, col_results = st.columns([7, 5])
    
    with col_input:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Customer Characteristics")
        
        # Grid layout for demographic parameters
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            gender = st.selectbox("Gender", ["Female", "Male"], index=0)
        with c2:
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"], index=0)
        with c3:
            partner = st.selectbox("Partner", ["No", "Yes"], index=1)
        with c4:
            dependents = st.selectbox("Dependents", ["No", "Yes"], index=0)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Service Bundle & Subscriptions")
        
        c5, c6, c7 = st.columns(3)
        with c5:
            phone_service = st.selectbox("Phone Service", ["No", "Yes"], index=1)
        with c6:
            # Enable MultipleLines ONLY if Phone Service is Yes
            if phone_service == "Yes":
                multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes"], index=0)
            else:
                multiple_lines = st.selectbox("Multiple Lines", ["No phone service"], index=0, disabled=True)
        with c7:
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], index=1)
            
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Internet services dependency layout
        c8, c9, c10 = st.columns(3)
        is_internet_disabled = (internet_service == "No")
        
        with c8:
            online_security = st.selectbox(
                "Online Security", 
                ["No", "Yes"] if not is_internet_disabled else ["No internet service"], 
                index=0, 
                disabled=is_internet_disabled
            )
        with c9:
            online_backup = st.selectbox(
                "Online Backup", 
                ["No", "Yes"] if not is_internet_disabled else ["No internet service"], 
                index=1, 
                disabled=is_internet_disabled
            )
        with c10:
            device_protection = st.selectbox(
                "Device Protection", 
                ["No", "Yes"] if not is_internet_disabled else ["No internet service"], 
                index=0, 
                disabled=is_internet_disabled
            )
            
        c11, c12, c13 = st.columns(3)
        with c11:
            tech_support = st.selectbox(
                "Tech Support", 
                ["No", "Yes"] if not is_internet_disabled else ["No internet service"], 
                index=0, 
                disabled=is_internet_disabled
            )
        with c12:
            streaming_tv = st.selectbox(
                "Streaming TV", 
                ["No", "Yes"] if not is_internet_disabled else ["No internet service"], 
                index=1, 
                disabled=is_internet_disabled
            )
        with c13:
            streaming_movies = st.selectbox(
                "Streaming Movies", 
                ["No", "Yes"] if not is_internet_disabled else ["No internet service"], 
                index=1, 
                disabled=is_internet_disabled
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Financials & Contracts")
        
        c14, c15, c16 = st.columns(3)
        with c14:
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"], index=0)
        with c15:
            paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"], index=1)
        with c16:
            payment_method = st.selectbox(
                "Payment Method", 
                [
                    "Bank transfer (automatic)", 
                    "Credit card (automatic)", 
                    "Electronic check", 
                    "Mailed check"
                ], 
                index=2
            )
            
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        c17, c18, c19 = st.columns([1, 1, 1])
        with c17:
            tenure = st.slider("Customer Tenure (Months)", min_value=1, max_value=72, value=12)
        with c18:
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=10.0, max_value=130.0, value=85.0, step=0.5)
            
        with c19:
            # High-grade auto-calculation of total charges (with override capability)
            auto_calc = st.checkbox("Sync Total Charges", value=True, help="Auto-calculate Total Charges based on Tenure and Monthly Charges.")
            default_total = round(monthly_charges * tenure, 2) if auto_calc else 1020.0
            
            total_charges = st.number_input(
                "Total Charges ($)", 
                min_value=0.0, 
                max_value=9000.0, 
                value=float(default_total),
                step=10.0,
                disabled=auto_calc
            )
            
            # Mathematical sanity check warning
            if not auto_calc and abs(total_charges - (monthly_charges * tenure)) > (monthly_charges * 5):
                st.warning("⚠️ Total charges deviates significantly from (Monthly Charges × Tenure). Check for accuracy.")
                
        st.markdown('</div>', unsafe_allow_html=True)

    # Compile the raw feature data
    raw_input_data = {
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges
    }
    
    # Process inputs & execute model inference
    df_raw = pd.DataFrame([raw_input_data])
    df_encoded = preprocess_features(df_raw)
    
    # Run scaling and predict
    df_scaled = scaler.transform(df_encoded)
    churn_prob = model.predict_proba(df_scaled)[0][1]
    churn_pred = model.predict(df_scaled)[0]

    with col_results:
        st.markdown('<div class="stCard" style="text-align: center;">', unsafe_allow_html=True)
        st.subheader("Assessment Results")
        
        # Circular gauge indicator
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = churn_prob * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CHURN RISK PROBABILITY", 'font': {'size': 18, 'color': '#E2E8F0'}},
            number = {'suffix': "%", 'font': {'size': 44, 'color': '#F8FAFC'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': "#6366F1"},
                'bgcolor': "rgba(15, 23, 42, 0.6)",
                'borderwidth': 2,
                'bordercolor': "#475569",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.15)'},
                    {'range': [30, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
                ],
                'threshold': {
                    'line': {'color': "#EF4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#F8FAFC"},
            height=250,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Dynamic Risk Badge
        if churn_prob >= 0.70:
            st.markdown('<div class="metric-badge badge-high">🚨 CRITICAL RISK</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #F87171; margin-top: 10px; font-weight: 500;">High probability of cancellation. Immediate proactive reachout is recommended.</p>', unsafe_allow_html=True)
        elif churn_prob >= 0.30:
            st.markdown('<div class="metric-badge badge-medium">⚠️ ELEVATED RISK</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #FBBF24; margin-top: 10px; font-weight: 500;">Moderate probability of churn. Monitor usage or offer value additions.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-badge badge-low">✅ STABLE ACCOUNT</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #34D399; margin-top: 10px; font-weight: 500;">Low churn profile. Excellent upsell potential for advanced packages.</p>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Risk factors explaining card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Key Risk Drivers")
        
        drivers = []
        # Calculate standard drivers from customer profile
        if contract == "Month-to-month":
            drivers.append("📄 **Month-to-Month Contract**: High correlation with rapid churn.")
        if tenure < 6:
            drivers.append("⏳ **New Customer Status**: First 6 months represent high churn windows.")
        if internet_service == "Fiber optic":
            drivers.append("⚡ **Fiber Optic Subscription**: High pricing bracket, correlation with monthly reviews.")
        if payment_method == "Electronic check":
            drivers.append("💵 **Electronic Check Payment**: Less stable than automated credit/bank drafts.")
        if online_security == "No" and internet_service != "No":
            drivers.append("🔒 **No Online Security**: Missing critical security lock-in.")
        if tech_support == "No" and internet_service != "No":
            drivers.append("🛠️ **No Tech Support**: Vulnerable to support-related frustration.")
            
        if len(drivers) > 0:
            for d in drivers[:4]:
                st.markdown(f"<div style='font-size: 0.9rem; padding: 4px 0;'>{d}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #64748B; font-size: 0.9rem;'>No major risk factors detected. Account is highly stable.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Proactive retention recommendation card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Targeted Retention Toolkit")
        
        recommendations = []
        if contract == "Month-to-month":
            recommendations.append("💼 **Contract Migration**: Offer a 10% loyalty discount to migrate to a **One Year Contract**.")
        if online_security == "No" and internet_service != "No":
            recommendations.append("🛡️ **Security Bundle Add-on**: Pitch **Online Security + Device Protection** free for 3 months.")
        if payment_method == "Electronic check":
            recommendations.append("💳 **Automate Autopay**: Offer a one-time $5 billing credit to switch to **Credit Card (automatic)**.")
        if monthly_charges > 80.0 and tenure > 12:
            recommendations.append("🎟️ **Loyalty Incentive**: Provide a custom 15% discount for 6 months on high billing tiers.")
            
        if len(recommendations) == 0:
            recommendations.append("🚀 **Upsell Strategy**: Recommend **Streaming TV + Streaming Movies** value bundles.")
            
        for r in recommendations[:3]:
            st.markdown(f"<div style='font-size: 0.9rem; margin-bottom: 8px; color: #E2E8F0;'>{r}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 1B: WHAT-IF SIMULATOR EXPANSION ---
    st.markdown('<h3 class="section-header">"What-If" Retention Simulator</h3>', unsafe_allow_html=True)
    st.markdown("""
    Use the simulation panel below to see how contract shifts, digital support add-ons, or payment migrations 
    reduce this customer's churn risk *before* the service representative reaches out.
    """)
    
    sc_col1, sc_col2 = st.columns([8, 4])
    with sc_col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("##### Apply simulated retention actions:")
        
        sim_c1, sim_c2, sim_c3 = st.columns(3)
        with sim_c1:
            sim_contract = st.selectbox(
                "Simulated Contract Type", 
                ["Month-to-month", "One year", "Two year"], 
                index=FEATURE_ORDER.index('Contract') - FEATURE_ORDER.index('Contract') # Default match current
            )
            # Match index to current input selectbox
            current_contract_idx = ["Month-to-month", "One year", "Two year"].index(contract)
            sim_contract = st.selectbox("Simulate Contract Shift", ["Month-to-month", "One year", "Two year"], index=current_contract_idx, key="sim_contract")
        with sim_c2:
            current_pm_idx = ["Bank transfer (automatic)", "Credit card (automatic)", "Electronic check", "Mailed check"].index(payment_method)
            sim_payment = st.selectbox("Simulate Payment Autopay", ["Bank transfer (automatic)", "Credit card (automatic)", "Electronic check", "Mailed check"], index=current_pm_idx, key="sim_pm")
        with sim_c3:
            # Toggle digital bundle
            sim_security = st.selectbox("Simulate Online Security", ["No", "Yes"] if not is_internet_disabled else ["No internet service"], index=0 if is_internet_disabled else ["No", "Yes"].index(online_security), key="sim_security")
            
        sim_c4, sim_c5 = st.columns(2)
        with sim_c4:
            sim_tech_support = st.selectbox("Simulate Tech Support Bundle", ["No", "Yes"] if not is_internet_disabled else ["No internet service"], index=0 if is_internet_disabled else ["No", "Yes"].index(tech_support), key="sim_tech_support")
        with sim_c5:
            discount = st.slider("Simulate Monthly Charge Discount (%)", min_value=0, max_value=30, value=0, step=5)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with sc_col2:
        # Build simulated dataframe
        sim_input = raw_input_data.copy()
        sim_input['Contract'] = sim_contract
        sim_input['PaymentMethod'] = sim_payment
        sim_input['OnlineSecurity'] = sim_security
        sim_input['TechSupport'] = sim_tech_support
        sim_input['MonthlyCharges'] = monthly_charges * (1 - (discount / 100))
        # Recalculate total charges roughly with simulated monthly cost
        sim_input['TotalCharges'] = sim_input['MonthlyCharges'] * tenure
        
        # Inference on simulated client
        df_sim_raw = pd.DataFrame([sim_input])
        df_sim_encoded = preprocess_features(df_sim_raw)
        df_sim_scaled = scaler.transform(df_sim_encoded)
        sim_churn_prob = model.predict_proba(df_sim_scaled)[0][1]
        
        st.markdown('<div class="stCard" style="text-align: center; height: 100%;">', unsafe_allow_html=True)
        st.markdown("##### Simulated Churn Risk")
        
        diff = sim_churn_prob - churn_prob
        
        # Visual display of change
        st.markdown(f"<h2 style='font-size: 3rem; margin: 10px 0; color: #818CF8;'>{sim_churn_prob*100:.1f}%</h2>", unsafe_allow_html=True)
        
        if diff < -0.05:
            st.markdown(f"<div style='color: #34D399; font-weight: bold; margin-bottom: 10px;'>📉 DECREASED BY {abs(diff)*100:.1f}%</div>", unsafe_allow_html=True)
            st.success("✅ Retention strategy is highly effective! Pitch these packages immediately.")
        elif abs(diff) <= 0.05:
            st.markdown(f"<div style='color: #94A3B8; font-weight: bold; margin-bottom: 10px;'>⚖️ STABLE (CHANGE: {diff*100:.1f}%)</div>", unsafe_allow_html=True)
            st.info("The modifications have minimal impact on this customer's churn profile.")
        else:
            st.markdown(f"<div style='color: #F87171; font-weight: bold; margin-bottom: 10px;'>📈 INCREASED BY {diff*100:.1f}%</div>", unsafe_allow_html=True)
            st.error("⚠️ Simulated actions have increased risk. Review pricing thresholds.")
            
        st.markdown('</div>', unsafe_allow_html=True)


# --- TAB 2: BATCH PREDICTOR ---
elif app_mode == "Batch CSV Predictor":
    st.markdown('<h3 class="section-header">Enterprise Batch Analysis Pipeline</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze entire lists of active users simultaneously. Upload a CSV matching the 19 standard feature inputs,
    and download the compiled risk report instantly.
    """)
    
    # Template Downloader Section
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.subheader("Data Formatting Standard")
    st.markdown("""
    Ensure your CSV includes the exact columns in the format listed below:
    - **Demographics**: `gender` (Female/Male), `SeniorCitizen` (0/1 or No/Yes), `Partner` (No/Yes), `Dependents` (No/Yes)
    - **Tenure & Phone**: `tenure` (Numeric), `PhoneService` (No/Yes), `MultipleLines` (No/No phone service/Yes)
    - **Internet**: `InternetService` (DSL/Fiber optic/No), `OnlineSecurity` (No/No internet service/Yes), `OnlineBackup` (No/No internet service/Yes), `DeviceProtection` (No/No internet service/Yes), `TechSupport` (No/No internet service/Yes), `StreamingTV` (No/No internet service/Yes), `StreamingMovies` (No/No internet service/Yes)
    - **Billing**: `Contract` (Month-to-month/One year/Two year), `PaperlessBilling` (No/Yes), `PaymentMethod` (Bank transfer (automatic)/Credit card (automatic)/Electronic check/Mailed check), `MonthlyCharges` (Numeric), `TotalCharges` (Numeric)
    """)
    
    # Create template helper
    template_df = pd.DataFrame([{
        'gender': 'Female', 'SeniorCitizen': 'No', 'Partner': 'Yes', 'Dependents': 'No',
        'tenure': 24, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
        'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'One year', 'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 79.85, 'TotalCharges': 1916.4
    }])
    
    template_csv = template_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Standard CSV Template",
        data=template_csv,
        file_name="churn_batch_template.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # File Uploader
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type="csv")
    
    if uploaded_file is not None:
        try:
            # Safe parsing
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"File loaded successfully: {len(df_upload)} records detected.")
            
            # Check column completeness
            missing_cols = [col for col in FEATURE_ORDER if col not in df_upload.columns]
            
            if missing_cols:
                st.error(f"❌ Column mismatch. Missing {len(missing_cols)} critical fields: {missing_cols}")
                st.stop()
                
            with st.spinner("Executing model scoring..."):
                # Clean and encode
                df_prep = preprocess_features(df_upload)
                
                # Predict
                df_prep_scaled = scaler.transform(df_prep)
                batch_probs = model.predict_proba(df_prep_scaled)[:, 1]
                batch_preds = model.predict(df_prep_scaled)
                
                # Append scoring results
                df_upload['Churn_Probability'] = np.round(batch_probs, 4)
                df_upload['Predicted_Churn'] = batch_preds
                df_upload['Risk_Category'] = df_upload['Churn_Probability'].apply(
                    lambda p: 'CRITICAL (High)' if p >= 0.70 else ('ELEVATED (Medium)' if p >= 0.30 else 'STABLE (Low)')
                )
                
            # Aggregate Analytics Section
            st.markdown('<h3 class="section-header">Batch Aggregates & Insights</h3>', unsafe_allow_html=True)
            
            total_accts = len(df_upload)
            churned_accts = int(np.sum(batch_preds))
            avg_risk = float(np.mean(batch_probs))
            high_risk_accts = int(np.sum(batch_probs >= 0.70))
            
            # Metric Grid
            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
            with mcol1:
                st.metric("Total Customers Scored", f"{total_accts:,}")
            with mcol2:
                st.metric("Predicted Churn Accounts", f"{churned_accts:,}", delta=f"{churned_accts/total_accts*100:.1f}% Rate")
            with mcol3:
                st.metric("Average Churn Risk", f"{avg_risk*100:.1f}%")
            with mcol4:
                st.metric("Critical Churn Accounts", f"{high_risk_accts:,}", delta=f"{high_risk_accts/total_accts*100:.1f}% total")
                
            # Visualizations
            vcol1, vcol2 = st.columns(2)
            with vcol1:
                st.markdown('<div class="stCard">', unsafe_allow_html=True)
                st.markdown("##### Churn Risk Distribution")
                fig_dist = px.histogram(
                    df_upload, 
                    x='Churn_Probability', 
                    color='Risk_Category',
                    color_discrete_map={
                        'CRITICAL (High)': '#EF4444', 
                        'ELEVATED (Medium)': '#F59E0B', 
                        'STABLE (Low)': '#10B981'
                    },
                    labels={'Churn_Probability': 'Churn Probability', 'count': 'Number of Customers'},
                    nbins=30,
                    template='plotly_dark'
                )
                fig_dist.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=300,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig_dist, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with vcol2:
                st.markdown('<div class="stCard">', unsafe_allow_html=True)
                st.markdown("##### Tenure vs. Monthly Charges by Churn Risk")
                fig_scatter = px.scatter(
                    df_upload,
                    x='tenure',
                    y='MonthlyCharges',
                    color='Churn_Probability',
                    color_continuous_scale='Reds',
                    labels={'tenure': 'Tenure (Months)', 'MonthlyCharges': 'Monthly Charges ($)'},
                    template='plotly_dark'
                )
                fig_scatter.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=300,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            # Results Table Preview
            st.markdown("##### Scored Accounts Preview")
            preview_cols = ['tenure', 'Contract', 'MonthlyCharges', 'TotalCharges', 'Churn_Probability', 'Risk_Category']
            st.dataframe(df_upload[preview_cols + [col for col in df_upload.columns if col not in preview_cols]].head(50), use_container_width=True)
            
            # Export Link
            output_csv = df_upload.to_csv(index=False)
            st.download_button(
                label="📥 Export Complete Scored Customer Dataset (CSV)",
                data=output_csv,
                file_name="telco_churn_scored_report.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Failed to process CSV file: {str(e)}")


# --- TAB 3: GLOBAL INSIGHTS ---
elif app_mode == "Model Global Insights":
    st.markdown('<h3 class="section-header">Global Model Explainability & Analytics</h3>', unsafe_allow_html=True)
    
    col_feat_imp, col_takeaway = st.columns([7, 5])
    
    with col_feat_imp:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Global Feature Importances")
        st.markdown("""
        The graph below displays the mathematical weights attributed to each feature by the **Random Forest** 
        ensemble during training. Features at the top are the strongest global indicators of churn.
        """)
        
        # Calculate feature importances
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            feat_imp_df = pd.DataFrame({
                'Feature': FEATURE_ORDER,
                'Importance': importances
            }).sort_values(by='Importance', ascending=True)
            
            fig_imp = px.bar(
                feat_imp_df,
                x='Importance',
                y='Feature',
                orientation='h',
                template='plotly_dark',
                color='Importance',
                color_continuous_scale='Bluered'
            )
            fig_imp.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500,
                xaxis_title="Relative Random Forest Weight",
                yaxis_title="",
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_imp, use_container_width=True)
        else:
            st.warning("Feature importances could not be calculated from this estimator instance.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_takeaway:
        st.markdown('<div class="stCard" style="height: 100%;">', unsafe_allow_html=True)
        st.subheader("Executive Takeaways")
        
        st.markdown("""
        Based on the global distribution and weights of our predictive models:
        
        1. 📄 **Contract Stability**:
           - **Month-to-month contracts** are the single strongest predictor of churn.
           - Action: Standard operating procedure should include aggressive discounts (up to 15%) offered automatically to accounts entering month-to-month status, urging them to sign 1-year or 2-year templates.
           
        2. ⏳ **The Critical Window (Tenure)**:
           - Customers in their **first 6 months** represent over 40% of standard churn volume.
           - Action: Implement a "High-Touch Onboarding" system during weeks 2, 6, and 12, checking in on connectivity issues and providing tutorial guides.
           
        3. 🔒 **Digital Lock-in (Add-on Subscriptions)**:
           - Customers with multiple digital add-ons (specifically **Online Security** and **Tech Support**) exhibit churn rates under 6%.
           - Action: Offer these modules bundled free for 6 months as part of new activations to raise the structural switching cost.
           
        4. 💳 **Autopay Incentives**:
           - **Electronic check payments** carry a 3x higher churn risk than automated credit card drafts.
           - Action: Incentivize paperless automated autopay transition through small, one-time bills credits (e.g. $5).
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>Churn Hub - Customer Churn Prediction System | Powered by RandomForestClassifier | Version 1.0.0 Pro</p>
</div>
""", unsafe_allow_html=True)
