"""
View module for the Batch CSV Predictor.
Handles user bulk dataset loading, feature alignment checks, predictive aggregation, 
Plotly visualization, and formatted CSV export download hooks.
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from typing import Any
from src.config import FEATURE_ORDER
from src.utils import preprocess_features


def render_batch_predictor_view(model: Any, scaler: Any) -> None:
    """
    Renders batch upload inputs, executes scikit-learn batch models, renders
    Plotly charts (distributions + scatters), and outputs CSV reports.

    Args:
        model: Loaded Random Forest classifier instance.
        scaler: Loaded StandardScaler scaling pipeline instance.
    """
    st.markdown('<h3 class="section-header">Enterprise Batch Analysis Pipeline</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    Analyze entire lists of active users simultaneously. Upload a CSV matching the 19 standard feature inputs,
    and download the compiled risk report instantly.
    """)
    
    # 1. Template Downloader Card
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.subheader("Data Formatting Standard")
    st.markdown("""
    Ensure your CSV includes the exact columns in the format listed below:
    - **Demographics**: `gender` (Female/Male), `SeniorCitizen` (0/1 or No/Yes), `Partner` (No/Yes), `Dependents` (No/Yes)
    - **Tenure & Phone**: `tenure` (Numeric), `PhoneService` (No/Yes), `MultipleLines` (No/No phone service/Yes)
    - **Internet**: `InternetService` (DSL/Fiber optic/No), `OnlineSecurity` (No/No internet service/Yes), `OnlineBackup` (No/No internet service/Yes), `DeviceProtection` (No/No internet service/Yes), `TechSupport` (No/No internet service/Yes), `StreamingTV` (No/No internet service/Yes), `StreamingMovies` (No/No internet service/Yes)
    - **Billing**: `Contract` (Month-to-month/One year/Two year), `PaperlessBilling` (No/Yes), `PaymentMethod` (Bank transfer (automatic)/Credit card (automatic)/Electronic check/Mailed check), `MonthlyCharges` (Numeric), `TotalCharges` (Numeric)
    """)
    
    # Helper default dataframe
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

    # 2. File Uploader UI widget
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type="csv")
    
    if uploaded_file is not None:
        try:
            # Parse sheet safely
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"File loaded successfully: {len(df_upload)} records detected.")
            
            # Verify feature completeness
            missing_cols = [col for col in FEATURE_ORDER if col not in df_upload.columns]
            if missing_cols:
                st.error(f"❌ Column mismatch. Missing {len(missing_cols)} critical fields: {missing_cols}")
                st.stop()
                
            with st.spinner("Executing model scoring..."):
                # Clean, map categories, and index sequence
                df_prep = preprocess_features(df_upload)
                
                # Execute Scaling & Ensemble Models
                df_prep_scaled = scaler.transform(df_prep)
                batch_probs = model.predict_proba(df_prep_scaled)[:, 1]
                batch_preds = model.predict(df_prep_scaled)
                
                # Append predicted properties to sheet
                df_upload['Churn_Probability'] = np.round(batch_probs, 4)
                df_upload['Predicted_Churn'] = batch_preds
                df_upload['Risk_Category'] = df_upload['Churn_Probability'].apply(
                    lambda p: 'CRITICAL (High)' if p >= 0.70 else ('ELEVATED (Medium)' if p >= 0.30 else 'STABLE (Low)')
                )
                
            # 3. Dynamic Aggregations Dashboard Section
            st.markdown('<h3 class="section-header">Batch Aggregates & Insights</h3>', unsafe_allow_html=True)
            
            total_accts = len(df_upload)
            churned_accts = int(np.sum(batch_preds))
            avg_risk = float(np.mean(batch_probs))
            high_risk_accts = int(np.sum(batch_probs >= 0.70))
            
            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
            with mcol1:
                st.metric("Total Customers Scored", f"{total_accts:,}")
            with mcol2:
                st.metric(
                    "Predicted Churn Accounts", 
                    f"{churned_accts:,}", 
                    delta=f"{churned_accts/total_accts*100:.1f}% Rate",
                    delta_color="inverse"
                )
            with mcol3:
                st.metric("Average Churn Risk", f"{avg_risk*100:.1f}%")
            with mcol4:
                st.metric(
                    "Critical Churn Accounts", 
                    f"{high_risk_accts:,}", 
                    delta=f"{high_risk_accts/total_accts*100:.1f}% total",
                    delta_color="inverse"
                )
                
            # 4. Plots grid
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
                
            # 5. Scored Explorer Table
            st.markdown("##### Scored Accounts Preview")
            preview_cols = ['tenure', 'Contract', 'MonthlyCharges', 'TotalCharges', 'Churn_Probability', 'Risk_Category']
            st.dataframe(
                df_upload[preview_cols + [col for col in df_upload.columns if col not in preview_cols]].head(50), 
                use_container_width=True
            )
            
            # Export download button
            output_csv = df_upload.to_csv(index=False)
            st.download_button(
                label="📥 Export Complete Scored Customer Dataset (CSV)",
                data=output_csv,
                file_name="telco_churn_scored_report.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Failed to process bulk CSV dataset: {str(e)}")
