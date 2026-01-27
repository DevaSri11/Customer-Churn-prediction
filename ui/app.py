import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from streamlit_option_menu import option_menu
from src.utils.data_helper import initialize_session_state
from ui.views.dashboard import render_dashboard
from ui.views.prediction import render_single_prediction, render_bulk_prediction

# Page Config
st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Feel
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(0,0,0,0.2);
    }
    
    /* Metrics */
    .stMetric {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f6;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
initialize_session_state()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4144/4144517.png", width=50)
    st.title("Churn Intelligence")
    
    page = option_menu(
        "Navigation", 
        ["Dashboard", "Single User Prediction", "Bulk Prediction"],
        icons=['speedometer2', 'person', 'cloud-upload'],
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#eee", "color": "#4b6cb7"},
            "nav-link-selected": {"background": "linear-gradient(90deg, #4b6cb7 0%, #182848 100%)", "color": "white"},
        }
    )
    


# Routing
if page == "Dashboard":
    render_dashboard()
elif page == "Single User Prediction":
    render_single_prediction()
elif page == "Bulk Prediction":
    render_bulk_prediction()
