import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

def get_ai_response(system_role, prompt, temperature=0.4):
    client = get_client()
    if not client:
        return "Error: GROQ_API_KEY not found. Please set it in your environment or Streamlit secrets."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling AI: {str(e)}"

def analyze_risk_factors(metrics_text, probability):
    prompt = f"""
    You are a churn analysis expert.
    
    Churn Probability: {probability:.2%}
    
    User Behaviour Metrics:
    {metrics_text}
    
    Identify the key churn risk factors for this user.
    Return them as concise bullet points.
    """
    return get_ai_response("You are a churn analysis expert.", prompt, 0.3)

def get_primary_churn_reason(risk_factors):
    prompt = f"""
    You are a churn analysis expert.
    
    Risk Factors:
    {risk_factors}
    
    Identify the ONE primary reason for churn in 5 words or less.
    """
    return get_ai_response("You analyze churn reasons.", prompt, 0.3)

def get_ai_retention_suggestions(churn_reason, risk_factors, churn_probability):
    prompt = f"""
    You are a senior product manager at a competitive coding platform
    like CodeChef or LeetCode.

    User churn probability: {churn_probability:.2%}

    Primary churn reason: {churn_reason}

    Observed risk factors:
    {risk_factors}

    Based on the churn reason, suggest 3-5 VERY SPECIFIC,
    realistic retention actions used by coding platforms.

    Guidelines:
    - Avoid generic suggestions
    - Focus on coding practice, contests, DSA learning, and motivation
    - Suggestions should be actionable and platform-specific
    - MATCH THIS STYLE:
      * "Recommend beginner-tagged problems similar to previously attempted ones"
      * "Unlock editor hints for next 5 problems"
      * "Add user to a '7-day DSA fundamentals' challenge"
      * "Show community solutions after 3 failed submissions"
    """

    return get_ai_response("You design retention strategies for coding platforms.", prompt, 0.3)

def analyze_dataset_insights(summary):
    prompt = f"""
    You are a senior product analyst.
    
    Dataset Summary:
    {summary}
    
    Identify:
    1. Major churn drivers
    2. High-risk user segments
    3. Actionable retention insights
    """
    return get_ai_response("You analyze product analytics datasets.", prompt, 0.4)
