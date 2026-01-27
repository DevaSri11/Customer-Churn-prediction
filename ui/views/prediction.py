import streamlit as st
import pandas as pd
import math
from src.utils.data_helper import get_active_data, load_default_data, load_model
from src.utils.ai_helper import analyze_risk_factors, get_primary_churn_reason, get_ai_retention_suggestions

def render_single_prediction():
    st.title("Single User Prediction")
    st.markdown("Predict churn probability for a specific user and get retention advice.")
    
    model = load_model()
    if model is None:
        st.error("Model not loaded. Cannot predict.")
        return

    # Check for selected user from Bulk Prediction
    defaults = {}
    if "selected_user_data" in st.session_state:
        defaults = st.session_state["selected_user_data"]
        st.info("Using data from selected user in Bulk Prediction.", icon="👤")
        if st.button("Clear Selection & Reset"):
            del st.session_state["selected_user_data"]
            st.rerun()

    with st.expander("User inputs", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            days_active = st.number_input("Days Active", 0, 3650, int(defaults.get("days_active", 20)))
            sessions_count = st.number_input("Sessions Count", 0, 10000, int(defaults.get("sessions_count", 40)))
            last_active_days = st.number_input("Days Since Last Activity", 0, 365, int(defaults.get("last_active_days", 10)))
            paywall_hits = st.number_input("Paywall Hits", 0, 500, int(defaults.get("paywall_hits", 5)))

        with col2:
            tasks_attempted = st.number_input("Tasks Attempted", 0, 5000, int(defaults.get("tasks_attempted", 50)))
            tasks_completed = st.number_input("Tasks Completed", 0, 5000, int(defaults.get("tasks_completed", 30)))
            failure_rate = st.slider("Failure Rate", 0.0, 1.0, float(defaults.get("failure_rate", 0.3)))
            solution_locked_hits = st.number_input("Solution Locked Hits", 0, 500, int(defaults.get("solution_locked_hits", 3)))

        with col3:
            avg_page_load_time = st.slider("Page Load Time (s)", 0.5, 60.0, float(defaults.get("avg_page_load_time", 3.0)))
            login_failures = st.number_input("Login Failures", 0, 100, int(defaults.get("login_failures", 2)))
            forced_relogin_count = st.number_input("Forced Re-logins", 0, 100, int(defaults.get("forced_relogin_count", 3)))

    # Prepare Data
    input_data = pd.DataFrame([{
        "days_active": days_active,
        "sessions_count": sessions_count,
        "last_active_days": last_active_days,
        "time_spent_learning": 300,
        "first_week_activity": 20,
        "completed_onboarding": 1,
        "tasks_attempted": tasks_attempted,
        "tasks_completed": tasks_completed,
        "failure_rate": failure_rate,
        "average_task_time": 40,
        "solution_view_attempts": 10,
        "solution_locked_hits": solution_locked_hits,
        "paywall_hits": paywall_hits,
        "paid_upgrade_done": 0,
        "dsa_sheet_access_attempts": 5,
        "avg_page_load_time": avg_page_load_time,
        "error_timeout_count": 2,
        "editor_video_crash_count": 1,
        "forced_relogin_count": forced_relogin_count,
        "login_failures": login_failures,
        "average_login_time": 5
    }])

    if st.button("Predict Churn Risk"):
        # Prediction Logic
        probability = model.predict_proba(input_data)[0][1]
        
        # Business Rule Override
        if last_active_days >= 21:
            probability = max(probability, 0.85)
            is_churn = True
            override_msg = " (Inactive > 21 days)"
        else:
            is_churn = probability >= 0.3
            override_msg = ""

        st.markdown("---")
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            if is_churn:
                st.error(f"⚠️ Likely to Churn{override_msg}")
            else:
                st.success("✅ Likely to Stay")
            st.metric("Churn Probability", f"{probability:.2%}")

        with res_col2:
            st.subheader("AI Risk Analysis")
            metrics_text = f"""
            Days active: {days_active}, Sessions: {sessions_count}
            Inactive days: {last_active_days}, Tasks: {tasks_completed}/{tasks_attempted}
            Failure Rate: {failure_rate}, Paywall hits: {paywall_hits}
            Page load time: {avg_page_load_time}s
            """
            
            with st.spinner("Consulting AI expert..."):
                risks = analyze_risk_factors(metrics_text, probability)
                st.write(risks)
                
        st.subheader("Retention Strategy")
        with st.spinner("Generating strategy..."):
            churn_reason = get_primary_churn_reason(risks)
            suggestions = get_ai_retention_suggestions(churn_reason, risks, probability)
            st.info(suggestions)


def render_bulk_prediction():
    st.title("Bulk Churn Prediction")
    st.markdown("Upload a CSV file to predict churn for multiple users. **Using this file ensures the Dashboard also updates.**")
    
    model = load_model()
    default_data = load_default_data()

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Update session state with uploaded file
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["active_data"] = df
            st.success("✅ Dashboard & Analytics updated with uploaded data!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return
    else:
        # Use whatever is active (could be default or previously uploaded)
        df = get_active_data()
        if df is not None:
            if default_data is not None and df.equals(default_data):
                st.info("Using default dataset.")
            else:
                st.info("Using currently active (uploaded) dataset.")
        else:
            st.warning("No data available.")
            return

    if st.button("Run Bulk Prediction"):
        if model:
            feature_cols = model.feature_names_in_
            # Ensure columns exist
            missing = [c for c in feature_cols if c not in df.columns]
            if missing:
                st.error(f"Missing columns in dataset: {missing}")
                return
                
            probs = model.predict_proba(df[feature_cols])[:, 1]
            df["churn_probability"] = probs
            df["risk_level"] = df["churn_probability"].apply(lambda x: "High" if x >= 0.3 else "Low")
            
            # Store in session state
            st.session_state["bulk_predictions_df"] = df
            st.rerun() # Rerun to show results immediately
        else:
            st.error("Model not loaded")

    # Display results if available in session state
    if "bulk_predictions_df" in st.session_state:
        result_df = st.session_state["bulk_predictions_df"]
        
        st.subheader("Prediction Results")
        
        # Pagination Controls
        items_per_page = 20
        total_items = len(result_df)
        total_pages = math.ceil(total_items / items_per_page)
        
        c_page, c_info = st.columns([1, 4])
        with c_page:
            current_page = st.number_input("Page Number", min_value=1, max_value=total_pages, value=1)
        with c_info:
            st.markdown(f"**Showing page {current_page} of {total_pages}** ({total_items} users)")

        start_idx = (current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        # Ensure user_id exists for display as 1-based index
        result_df["user_id"] = range(1, len(result_df) + 1)
        
        # Show slice
        cols_to_show = ["user_id", "churn_probability", "risk_level"] + [c for c in result_df.columns if c not in ["user_id", "churn_probability", "risk_level"]]
        sliced_df = result_df[cols_to_show].iloc[start_idx:end_idx]
        
        event = st.dataframe(
            sliced_df, 
            on_select="rerun", 
            selection_mode="single-row"
        )
        
        if len(event.selection.rows) > 0:
            selected_row_idx = event.selection.rows[0]
            # Convert view index to actual index in the slice, then to result_df index
            actual_row = sliced_df.iloc[selected_row_idx]
            
            st.session_state["selected_user_data"] = actual_row.to_dict()
            st.success(f"✅ User selected! Switch to 'Single User Prediction' tab to analyze.")
        
        st.markdown("---")
        # Download
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Full Predictions", csv, "churn_predictions.csv", "text/csv")
