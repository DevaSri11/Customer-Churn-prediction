import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils.data_helper import get_active_data, load_default_data, reset_data
from src.utils.ai_helper import analyze_dataset_insights

def render_dashboard():
    data = get_active_data()
    default_data = load_default_data()
    
    st.title("Product Analytics Dashboard")
    st.markdown("Insights into user activity, churn drivers, and platform health.")
    
    if data is None:
        st.info("Please upload data to view the dashboard.")
        return

    # Info banner if using custom data
    if default_data is not None and not data.equals(default_data):
        st.info("You are viewing insights for **custom uploaded data**.")
        if st.button("Reset to Default Dataset"):
            reset_data()
            st.rerun()

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    active_count = (data["last_active_days"] < 21).sum()
    inactive_count = (data["last_active_days"] >= 21).sum()
    
    with c1: st.metric("Active Users (<21 days)", active_count)
    with c2: st.metric("Inactive Users (21+ days)", inactive_count, delta=-int(inactive_count), delta_color="inverse")
    with c3: st.metric("Total Users", len(data))

    st.markdown("---")

    # Chart 1: Activity Status
    c_chart1, c_chart2 = st.columns(2)
    
    with c_chart1:
        st.subheader("User Status Distribution")
        status_df = pd.DataFrame({
            "Status": ["Active", "Inactive"],
            "Count": [active_count, inactive_count]
        })
        fig_status = px.bar(status_df, x="Status", y="Count", color="Status", 
                            color_discrete_sequence=["#2ecc71", "#e74c3c"],
                            title="Active vs Inactive Users")
        st.plotly_chart(fig_status, key="fig_status")

    with c_chart2:
        st.subheader("Inactivity Buckets")
        bins = [0, 7, 14, 21, 60]
        labels = ["0–7 days", "8–14 days", "15–21 days", "21+ days"]
        data["inactive_bucket"] = pd.cut(data["last_active_days"], bins=bins, labels=labels, right=False)
        bucket_counts = data["inactive_bucket"].value_counts().sort_index().reset_index()
        bucket_counts.columns = ["Days Since Last Active", "User Count"]
        
        fig_buckets = px.bar(bucket_counts, x="Days Since Last Active", y="User Count",
                             title="Inactivity Distribution",
                             color="User Count", color_continuous_scale="Viridis")
        st.plotly_chart(fig_buckets, key="fig_buckets")

    # Chart 2: Correlations
    st.markdown("Churn Drivers")
    col1, col2 = st.columns(2)
    
    if "churn" in data.columns:
        with col1:
            paywall_churn = data.groupby("paywall_hits")["churn"].mean().reset_index()
            fig_paywall = px.line(paywall_churn, x="paywall_hits", y="churn", markers=True,
                                  title="Paywall Hits vs Churn Rate",
                                  labels={"churn": "Churn Probability", "paywall_hits": "Paywall Hits"})
            st.plotly_chart(fig_paywall, key="fig_paywall")
            
        with col2:
            failure_churn = data.groupby("failure_rate")["churn"].mean().reset_index()
            fig_fail = px.line(failure_churn, x="failure_rate", y="churn", markers=True,
                               title="Failure Rate vs Churn Rate",
                               color_discrete_sequence=["#e67e22"])
            st.plotly_chart(fig_fail, key="fig_fail")
    else:
        st.info("Churn column not found in dataset. Some charts are disabled.")

    # AI Insights
    st.markdown("---")
    if st.button("Generate AI Dashboard Insights"):
        with st.spinner("Analyzing dataset patterns..."):
            summary = data.describe().to_string()
            insights = analyze_dataset_insights(summary)
            st.success("Analysis Complete")
            st.markdown(insights)
