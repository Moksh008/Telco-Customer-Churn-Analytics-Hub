"""
Global configuration module for the Telco Customer Churn Predictor.
Contains design styling (CSS), categorical dictionaries, and standard feature sequence parameters.
"""

import streamlit as st

# ==========================================
# 1. DESIGN STYLING CONFIGURATION (CSS)
# ==========================================
CUSTOM_CSS = """
<style>
    /* Global Background and Typography Overrides */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
    }
    
    /* Premium Glassmorphism main dashboard layout card */
    div.stCard {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    
    /* Premium visual banner for welcoming users */
    .hero-banner-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.15), inset 0 0 20px rgba(99, 102, 241, 0.1);
        backdrop-filter: blur(12px);
        margin-bottom: 30px;
        text-align: left;
    }
    
    /* Interactive Card layouts with hover transitions */
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
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .stCard-hover:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 16px 35px rgba(99, 102, 241, 0.28);
        border-color: rgba(99, 102, 241, 0.6);
    }
    
    /* Grid system metric items */
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
    
    /* Visual workflow pipeline step styling */
    .pipeline-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 20px 0;
        gap: 10px;
        width: 100%;
    }
    @media (max-width: 768px) {
        .pipeline-container {
            flex-direction: column;
            gap: 15px;
        }
        .pipeline-arrow {
            transform: rotate(90deg);
        }
    }
    .pipeline-step {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
        flex: 1;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .pipeline-step:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.15);
    }
    .pipeline-step-icon {
        font-size: 1.8rem;
        margin-bottom: 6px;
    }
    .pipeline-step-title {
        font-weight: 700;
        font-size: 0.88rem;
        color: #F8FAFC;
        margin-bottom: 4px;
    }
    .pipeline-step-desc {
        font-size: 0.75rem;
        color: #94A3B8;
        line-height: 1.4;
    }
    .pipeline-arrow {
        color: #818CF8;
        font-weight: bold;
        font-size: 1.5rem;
        text-shadow: 0 0 8px rgba(99, 102, 241, 0.4);
        user-select: none;
    }
    
    /* Interactive Launcher button rules inside grid cards */
    .card-launcher-btn {
        display: inline-block;
        width: 100%;
        text-align: center;
        padding: 10px 15px;
        background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%);
        color: white !important;
        font-weight: 700;
        font-size: 0.85rem;
        border-radius: 8px;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        margin-top: 15px;
    }
    .card-launcher-btn:hover {
        background: linear-gradient(90deg, #4F46E5 0%, #4338CA 100%);
        box-shadow: 0 8px 22px rgba(99, 102, 241, 0.5);
        transform: translateY(-2px);
    }
    
    /* Risk indicator tag badges */
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

    /* Customized Header styles */
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
        margin-top: 30px;
        margin-bottom: 15px;
    }
    
    /* Sidebar visual adjustments */
    div[data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Generic footer styling */
    .footer {
        text-align: center;
        padding: 30px 0 10px 0;
        color: #64748B;
        font-size: 0.85rem;
    }
    
    /* Custom override styling on standard buttons inside overview cards */
    .stCard-hover div.stButton button {
        background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%) !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        margin-top: 10px !important;
    }
    .stCard-hover div.stButton button:hover {
        background: linear-gradient(90deg, #4F46E5 0%, #4338CA 100%) !important;
        box-shadow: 0 8px 22px rgba(99, 102, 241, 0.5) !important;
        transform: translateY(-2px) !important;
        color: white !important;
    }
</style>
"""


def inject_custom_styles() -> None:
    """Injects high-quality typography stylesheet and theme CSS tags."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# 2. FEATURE ORDER & CATEGORICAL MAPS
# ==========================================
# Strict ordered array mapping to standard feature column indices for inference scaling
FEATURE_ORDER = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
]

# Encoding dictionaries mapped by random-forest algorithms
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

# Reverse mapping decoding dictionaries for human-readable outputs and default options
DECODING_MAPS = {
    feature: {val: key for key, val in mapping.items()} 
    for feature, mapping in ENCODING_MAPS.items()
}
