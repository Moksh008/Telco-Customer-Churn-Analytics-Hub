"""
Utility functions module for model loading, feature preprocessing, and business logic mapping.
Includes cached joblib loaders and rule-based diagnostic evaluation algorithms.
"""

import os
import joblib
import pandas as pd
import streamlit as st
from typing import Dict, Any, Tuple, Optional, List
from src.config import FEATURE_ORDER, ENCODING_MAPS


@st.cache_resource(show_spinner=True)
def load_ml_assets() -> Tuple[Optional[Any], Optional[Any], Optional[str]]:
    """
    Safely loads the machine learning random forest model and scaling pipeline.
    Uses st.cache_resource to cache binaries globally.

    Returns:
        Tuple: (classifier, scaler, error_message)
    """
    model_path = "churn_model.pkl"
    scaler_path = "scaler.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None, f"Asset files missing. Ensure {model_path} and {scaler_path} exist."
        
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler, None
    except Exception as e:
        return None, None, f"Failed to load scikit-learn binary packages: {str(e)}"


def preprocess_features(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Processes a raw DataFrame of human-readable inputs (e.g. 'Yes', 'No') into 
    its encoded numeric equivalent mapped in standard feature sequence order.

    Args:
        df_raw (pd.DataFrame): Raw dataframe with categorical features.

    Returns:
        pd.DataFrame: Scaler-ready encoded DataFrame in exact FEATURE_ORDER.
    """
    df_encoded = df_raw.copy()
    
    # 1. Apply category mappings
    for col, mapping in ENCODING_MAPS.items():
        if col in df_encoded.columns:
            df_encoded[col] = df_encoded[col].map(mapping).fillna(0).astype(int)
    
    # 2. Enforce standard continuous dtypes
    for c_col in ['tenure', 'MonthlyCharges', 'TotalCharges']:
        if c_col in df_encoded.columns:
            df_encoded[c_col] = pd.to_numeric(df_encoded[c_col]).fillna(0.0)
            
    return df_encoded[FEATURE_ORDER]


def get_risk_drivers(
    contract: str,
    tenure: int,
    internet_service: str,
    payment_method: str,
    online_security: str,
    tech_support: str
) -> List[str]:
    """
    Applies conditional expert heuristic checks on a subscriber's profile 
    to extract the primary driving factors for elevated/critical churn risk.

    Returns:
        List[str]: Formatted driver explanation strings.
    """
    drivers = []
    
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
        
    return drivers


def get_retention_recommendations(
    contract: str,
    online_security: str,
    internet_service: str,
    payment_method: str,
    monthly_charges: float,
    tenure: int
) -> List[str]:
    """
    Formulates a targeted list of prescriptive business retention recommendations 
    tailored to counter the customer's specific vulnerability flags.

    Returns:
        List[str]: Actionable business strategies.
    """
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
        
    return recommendations
