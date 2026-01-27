
import sys
import os

# Add project root to path to ensure imports work
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.utils.ai_helper import get_ai_response

def test_groq_connection():
    print("Testing Groq API connection...")
    try:
        response = get_ai_response(
            "You are a helpful assistant.", 
            "Respond with 'Groq API is working!' if you can hear me."
        )
        print("\nResponse from API:")
        print(response)
        
        if "Groq API is working" in response or "working" in response.lower():
            print("\nSUCCESS: Groq API connection verified!")
        else:
            print("\nWARNING: Unexpected response content.")
            
    except Exception as e:
        print(f"\nFAILURE: {str(e)}")

if __name__ == "__main__":
    test_groq_connection()
