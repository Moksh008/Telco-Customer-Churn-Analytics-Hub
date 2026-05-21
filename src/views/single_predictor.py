"""
View module for the Single Customer Predictor and "What-If" Retention Simulator.
Coordinates individual input controls, Plotly circular gauges, risk explanations, and retention remedies.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from typing import Any
from src.config import FEATURE_ORDER
from src.utils import (
    preprocess_features, 
    get_risk_drivers, 
    get_retention_recommendations
)


def render_single_predictor_view(model: Any, scaler: Any) -> None:
    """
    Renders input form columns and coordinates model inference, gauge indicators,
    remedy recipes, and the What-If retention simulation panel.

    Args:
        model: Loaded Random Forest classifier instance.
        scaler: Loaded StandardScaler scaling pipeline instance.
    """
    st.markdown('<h3 class="section-header">Interactive Risk Assessment & What-If Simulator</h3>', unsafe_allow_html=True)
    
    # 1. Primary Layout Columns
    col_input, col_results = st.columns([7, 5])
    
    with col_input:
        # A. Demographics Card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Customer Characteristics")
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
        
        # B. Service Bundle Subscriptions Card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Service Bundle & Subscriptions")
        c5, c6, c7 = st.columns(3)
        with c5:
            phone_service = st.selectbox("Phone Service", ["No", "Yes"], index=1)
        with c6:
            # Enable MultipleLines ONLY if Phone Service is active
            if phone_service == "Yes":
                multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes"], index=0)
            else:
                multiple_lines = st.selectbox("Multiple Lines", ["No phone service"], index=0, disabled=True)
        with c7:
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"], index=1)
            
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
        
        # Internet dependency conditional inputs
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
        
        # C. Financial Contract Details Card
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
            # High-grade auto-calculation of total charges (with override toggle)
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
            
            # Mathematical discrepancy warning
            if not auto_calc and abs(total_charges - (monthly_charges * tenure)) > (monthly_charges * 5):
                st.warning("⚠️ Total charges deviates significantly from (Monthly Charges × Tenure). Check for accuracy.")
                
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Extract & Encode Features
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
    
    df_raw = pd.DataFrame([raw_input_data])
    df_encoded = preprocess_features(df_raw)
    
    # 3. Random Forest Inference
    df_scaled = scaler.transform(df_encoded)
    churn_prob = model.predict_proba(df_scaled)[0][1]

    # 4. Results Column Rendering
    with col_results:
        st.markdown('<div class="stCard" style="text-align: center;">', unsafe_allow_html=True)
        st.subheader("Assessment Results")
        
        # Plotly Circular Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_prob * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "CHURN RISK PROBABILITY", 'font': {'size': 18, 'color': '#E2E8F0'}},
            number={'suffix': "%", 'font': {'size': 44, 'color': '#F8FAFC'}},
            gauge={
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
        
        # Churn Probability Risk Badges
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
        
        # Key Drivers Diagnostic List Card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Key Risk Drivers")
        drivers = get_risk_drivers(
            contract=contract,
            tenure=tenure,
            internet_service=internet_service,
            payment_method=payment_method,
            online_security=online_security,
            tech_support=tech_support
        )
        if drivers:
            for d in drivers[:4]:
                st.markdown(f"<div style='font-size: 0.9rem; padding: 4px 0;'>{d}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #64748B; font-size: 0.9rem;'>No major risk factors detected. Account is highly stable.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Proactive Prescriptions Recommendation Card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Targeted Retention Toolkit")
        recommendations = get_retention_recommendations(
            contract=contract,
            online_security=online_security,
            internet_service=internet_service,
            payment_method=payment_method,
            monthly_charges=monthly_charges,
            tenure=tenure
        )
        for r in recommendations[:3]:
            st.markdown(f"<div style='font-size: 0.9rem; margin-bottom: 8px; color: #E2E8F0;'>{r}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. What-If Simulation Panel Section
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
            current_contract_idx = ["Month-to-month", "One year", "Two year"].index(contract)
            sim_contract = st.selectbox("Simulate Contract Shift", ["Month-to-month", "One year", "Two year"], index=current_contract_idx, key="sim_contract")
        with sim_c2:
            current_pm_idx = ["Bank transfer (automatic)", "Credit card (automatic)", "Electronic check", "Mailed check"].index(payment_method)
            sim_payment = st.selectbox("Simulate Payment Autopay", ["Bank transfer (automatic)", "Credit card (automatic)", "Electronic check", "Mailed check"], index=current_pm_idx, key="sim_pm")
        with sim_c3:
            sim_security = st.selectbox("Simulate Online Security", ["No", "Yes"] if not is_internet_disabled else ["No internet service"], index=0 if is_internet_disabled else ["No", "Yes"].index(online_security), key="sim_security")
            
        sim_c4, sim_c5 = st.columns(2)
        with sim_c4:
            sim_tech_support = st.selectbox("Simulate Tech Support Bundle", ["No", "Yes"] if not is_internet_disabled else ["No internet service"], index=0 if is_internet_disabled else ["No", "Yes"].index(tech_support), key="sim_tech_support")
        with sim_c5:
            discount = st.slider("Simulate Monthly Charge Discount (%)", min_value=0, max_value=30, value=0, step=5)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with sc_col2:
        # Build simulated dataframe parameters
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
