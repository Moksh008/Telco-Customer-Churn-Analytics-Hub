"""
View module for the Churn Hub Welcome and Project Overview (Landing Page).
Renders glassmorphic hero banners, database metrics, interactive tabs guidance, and FAQ panels.
"""

import streamlit as st


def render_welcome_view() -> None:
    """Renders the standard premium homepage design and navigation prompts."""
    # 1. Ultra-Premium Glowing Hero Banner
    st.markdown("""
    <div class="hero-banner-card">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 12px;">
            <span style="font-size: 2.6rem; filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.75));">⚡</span>
            <h1 class="hero-title" style="margin: 0; font-size: 2.8rem; letter-spacing: -0.02em;">CHURN HUB</h1>
        </div>
        <p style="font-size: 1.12rem; color: #E2E8F0; line-height: 1.6; max-width: 850px; margin-bottom: 22px; font-family: 'Outfit', sans-serif;">
            An elite, production-grade AI portal for customer retention analytics. Infuse billing and operations 
            with proactive machine learning models to identify cancellation risks and prescribe high-yielding loyalty campaigns.
        </p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <span class="metric-badge" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3);">🚀 RandomForest Predictor</span>
            <span class="metric-badge" style="background: rgba(129, 140, 248, 0.15); color: #818CF8; border: 1px solid rgba(129, 140, 248, 0.3);">🌲 Ensemble Decision Trees</span>
            <span class="metric-badge" style="background: rgba(192, 132, 252, 0.15); color: #C084FC; border: 1px solid rgba(192, 132, 252, 0.3);">💎 Glassmorphic Operations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Key Metrics Grid
    st.markdown('<h3 class="section-header">📊 Sandbox Key Metrics</h3>', unsafe_allow_html=True)
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown("""
        <div class="main-metric-card" style="border-top: 4px solid #38BDF8; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1);">
            <div class="main-metric-value" style="background: linear-gradient(90deg, #38BDF8 0%, #06B6D4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">7,043</div>
            <div class="main-metric-label">Dataset Records</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol2:
        st.markdown("""
        <div class="main-metric-card" style="border-top: 4px solid #6366F1; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);">
            <div class="main-metric-value" style="background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">84.5%</div>
            <div class="main-metric-label">Inference ROC-AUC</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol3:
        st.markdown("""
        <div class="main-metric-card" style="border-top: 4px solid #F59E0B; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);">
            <div class="main-metric-value" style="background: linear-gradient(90deg, #F59E0B 0%, #D97706 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">26.5%</div>
            <div class="main-metric-label">Baseline Churn</div>
        </div>
        """, unsafe_allow_html=True)
    with mcol4:
        st.markdown("""
        <div class="main-metric-card" style="border-top: 4px solid #C084FC; box-shadow: 0 4px 15px rgba(192, 132, 252, 0.1);">
            <div class="main-metric-value" style="background: linear-gradient(90deg, #C084FC 0%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">19</div>
            <div class="main-metric-label">Input Parameters</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

    # 3. Two-Column Context Block
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
        
    # 4. Pipeline Steps
    st.markdown("""
    <h3 class="section-header">⚙️ Real-Time Retention Pipeline</h3>
    <div class="pipeline-container">
        <div class="pipeline-step">
            <div class="pipeline-step-icon" style="filter: drop-shadow(0 0 5px rgba(56, 189, 248, 0.4));">👥</div>
            <div class="pipeline-step-title" style="color: #38BDF8;">1. Profile Input</div>
            <div class="pipeline-step-desc">User enters customer details or uploads bulk CSV spreadsheet lists.</div>
        </div>
        <div class="pipeline-arrow">➡️</div>
        <div class="pipeline-step">
            <div class="pipeline-step-icon" style="filter: drop-shadow(0 0 5px rgba(99, 102, 241, 0.4));">⚖️</div>
            <div class="pipeline-step-title" style="color: #818CF8;">2. Processing</div>
            <div class="pipeline-step-desc">Applies alphabetical ordinal encoding & StandardScaler transformations.</div>
        </div>
        <div class="pipeline-arrow">➡️</div>
        <div class="pipeline-step">
            <div class="pipeline-step-icon" style="filter: drop-shadow(0 0 5px rgba(168, 85, 247, 0.4));">🌲</div>
            <div class="pipeline-step-title" style="color: #C084FC;">3. Random Forest</div>
            <div class="pipeline-step-desc">Ensemble calculates statistical risk probability via hundreds of trees.</div>
        </div>
        <div class="pipeline-arrow">➡️</div>
        <div class="pipeline-step">
            <div class="pipeline-step-icon" style="filter: drop-shadow(0 0 5px rgba(245, 158, 11, 0.4));">🎯</div>
            <div class="pipeline-step-title" style="color: #F59E0B;">4. Prescription</div>
            <div class="pipeline-step-desc">Proactive Retention Optimizer proposes targeted Loyalty Bundles.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. Dynamic Module Navigation Links
    st.markdown('<h3 class="section-header">Interactive Platform Navigation</h3>', unsafe_allow_html=True)
    guide_c1, guide_c2, guide_c3 = st.columns(3)
    
    with guide_c1:
        st.markdown("""
        <div class="stCard-hover" style="border-top: 4px solid #38BDF8;">
            <div>
                <h4 style="color: #38BDF8; font-weight: 700; margin-top: 0; margin-bottom: 10px;">👤 Single Predictor</h4>
                <p style="font-size: 0.92rem; line-height: 1.5; color: #CBD5E1; margin-bottom: 8px;">
                    <b>Designed for front-line reps and account specialists.</b>
                </p>
                <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 12px;">
                    Input individual customer features to get real-time churn predictions, key risk explanations, and 
                    targeted coupon/bundle solutions.
                </p>
                <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 15px;">
                    <b>Bonus Feature</b>: The <b>What-If Simulator</b> lets you test how changing a monthly contract to a one-year or two-year term mitigates churn!
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Single Predictor", key="btn_single"):
            st.session_state.app_mode = "Single Customer Predictor"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with guide_c2:
        st.markdown("""
        <div class="stCard-hover" style="border-top: 4px solid #F59E0B;">
            <div>
                <h4 style="color: #F59E0B; font-weight: 700; margin-top: 0; margin-bottom: 10px;">📁 Batch CSV Predictor</h4>
                <p style="font-size: 0.92rem; line-height: 1.5; color: #CBD5E1; margin-bottom: 8px;">
                    <b>Designed for database analysts and marketing directors.</b>
                </p>
                <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 12px;">
                    Upload a structured customer sheet to score hundreds of profiles simultaneously. 
                    View campaign aggregate counts, risk histograms, and scatter plots.
                </p>
                <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 15px;">
                    <b>Bonus Feature</b>: Instantly download the complete evaluated database as a scored spreadsheet report.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Launch Batch Predictor", key="btn_batch"):
            st.session_state.app_mode = "Batch CSV Predictor"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with guide_c3:
        st.markdown("""
        <div class="stCard-hover" style="border-top: 4px solid #818CF8;">
            <div>
                <h4 style="color: #818CF8; font-weight: 700; margin-top: 0; margin-bottom: 10px;">📊 Model Global Insights</h4>
                <p style="font-size: 0.92rem; line-height: 1.5; color: #CBD5E1; margin-bottom: 8px;">
                    <b>Designed for executives and business strategists.</b>
                </p>
                <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 12px;">
                    Review the global mathematical weights derived by the Random Forest model across 7,000+ accounts.
                </p>
                <p style="font-size: 0.88rem; line-height: 1.5; color: #94A3B8; margin-bottom: 15px;">
                    <b>Bonus Feature</b>: Provides direct, data-backed operational takeaways to structurally cure churn.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🧠 Launch Global Insights", key="btn_global"):
            st.session_state.app_mode = "Model Global Insights"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 6. FAQ Accordion Panels
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
