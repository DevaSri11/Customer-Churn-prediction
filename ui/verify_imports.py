import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

try:
    print("Testing imports...")
    from src.utils.data_helper import initialize_session_state
    from src.utils.ai_helper import get_ai_response
    from ui.views.dashboard import render_dashboard
    from ui.views.prediction import render_single_prediction
    print("Imports successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
