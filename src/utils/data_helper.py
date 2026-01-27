import os
import pandas as pd
import joblib
import streamlit as st

# -------------------------------------------------
# Paths & Loading
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "src", "churn_model.pkl")
# Try to find data in common locations
DATA_PATH_RAW = os.path.join(BASE_DIR, "data", "raw", "customer_churn_1000_users.xlsx")
DATA_PATH_CSV = os.path.join(BASE_DIR, "data", "raw", "customer_churn_1000_users.csv")

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        st.error(f"Model not found at {MODEL_PATH}")
        return None

@st.cache_data
def load_default_data():
    if os.path.exists(DATA_PATH_RAW):
        return pd.read_excel(DATA_PATH_RAW)
    elif os.path.exists(DATA_PATH_CSV):
        return pd.read_csv(DATA_PATH_CSV)
    else:
        # Just return None if not found, let UI handle warning
        return None

def initialize_session_state():
    if "active_data" not in st.session_state:
        default_data = load_default_data()
        st.session_state["active_data"] = default_data.copy() if default_data is not None else None

def get_active_data():
    return st.session_state.get("active_data")

def reset_data():
    default_data = load_default_data()
    if default_data is not None:
        st.session_state["active_data"] = default_data.copy()
