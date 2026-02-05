# Customer Churn Prediction for Coding Platforms

An end-to-end Churn Intelligence System that predicts user churn on competitive coding platforms (like CodeChef, LeetCode) using Machine Learning, and augments predictions with AI-powered explanations and personalized retention strategies.
This project combines **Machine Learning**, **Product Analytics Dashboards**, and **AI-powered explanations & retention strategies** to not only predict churn, but also explain *why* it happens and *what actions* can be taken to reduce it.

## Problem Statement

Coding platforms lose users due to the following reasons:

<ul>
  <li><b>Long inactivity</b> caused by loss of motivation or irregular practice</li>
  <li><b>Learning difficulty</b> and repeated failures while solving problems</li>
  <li><b>Paywall and locked-solution frustration</b> that blocks learning progress</li>
  <li><b>Platform performance issues</b> such as slow loading and crashes</li>
  <li><b>Login friction</b> including frequent re-logins and authentication failures</li>
</ul>
<b>Goal:</b>
<ul>
  <li>Predict churn risk using machine learning</li>
  <li>Explain <i>why</i> users are likely to churn</li>
  <li>Suggest <i>actionable, platform-specific retention strategies</i></li>
</ul>
<p>
Even though only a small percentage of users churn, this group has a
<b>high impact on engagement and revenue</b>, making early churn detection critical.
</p>

## What is “Churn” in This Project?

A user is considered **high churn risk** when they:

<ul>
  <li>Have been inactive for <b>21+ days</b></li>
  <li>Face repeated failures while solving problems</li>
  <li>Frequently encounter paywalls or locked solutions</li>
  <li>Experience slow platform performance or login issues</li>
</ul>

## Machine Learning Overview

<ul>
  <li><b>Type:</b> Supervised Classification</li>
  <li><b>Model:</b> Random Forest / Logistic Regression</li>
  <li><b>Target:</b> Churn (0 = Active, 1 = Churned)</li>
  <li><b>Output:</b> Churn Probability (0–100%)</li>
</ul>

## Dataset Overview

<ul>
  <li><b>Each row:</b> One user</li>
  <li><b>Data window:</b> Aggregated behavior over recent days/weeks</li>
  <li><b>Target column:</b> <code>churn</code> (0 = Active, 1 = Churned)</li>
</ul>

## Key Features Used

<ul>
  <li><b>Engagement:</b> days_active, sessions_count, last_active_days</li>
  <li><b>Learning Difficulty:</b> tasks_attempted, tasks_completed, failure_rate</li>
  <li><b>Paywall Friction:</b> paywall_hits, solution_locked_hits</li>
  <li><b>Platform Performance:</b> avg_page_load_time, error_timeout_count</li>
  <li><b>Login Issues:</b> login_failures, forced_relogin_count</li>
</ul>

## Product Analytics Dashboard

The dashboard provides key **product-level insights** to understand user behavior and churn patterns:

<ul>
  <li><b>Active vs Inactive Users</b> – Identifies overall engagement health</li>
  <li><b>Inactivity Buckets</b> – Categorizes users by last activity (0–7, 8–14, 15–21, 21+ days)</li>
  <li><b>Paywall Hits vs Churn Rate</b> – Shows impact of access barriers on churn</li>
  <li><b>Failure Rate vs Churn Rate</b> – Highlights learning difficulty as a churn driver</li>
</ul>

<p align="center">
  <img src="https://github.com/user-attachments/assets/0944cd54-a53e-41f4-a3e4-e486eb6f0021" width="48%" />
  <img src="https://github.com/user-attachments/assets/a1a0bfd6-31b0-4b53-8456-b5a5ee56f38c" width="48%" />
</p>

## Single User Churn Prediction
For an individual user, the system displays: 
<ul> <li>Churn probability</li>
  <li>High-risk or low-risk classification</li> 
  <li>AI-generated churn risk explanation</li> 
  <li>Personalized retention strategies</li> 
</ul> 
Example insights:
<i>“If a user struggles with free DSA problems, the AI suggests granting temporary access to solutions for two days to improve engagement.”</i>

<p align="center">
  <img src="https://github.com/user-attachments/assets/770b2b28-19dc-46f6-8da7-f29723aeb775" width="48%" />
  <img src="https://github.com/user-attachments/assets/d3e83e9f-bfe7-4957-b04f-1b6dd2305bfc" width="48%" />
</p>

## Bulk Churn Prediction

<ul>
  <li>Upload a CSV file with multiple users</li>
  <li>Predict churn probability for each user</li>
  <li>Classify users as <b>High Risk</b> or <b>Low Risk</b></li>
  <li>Download results with churn scores</li>
</ul>

<img width="1877" height="903" alt="Screenshot 2026-01-27 111710" src="https://github.com/user-attachments/assets/96535976-7e34-4a4f-b57e-76ea01cd03a4" />

## Folder Structure

<pre>
Customer-Churn-Prediction/
│
├── data/
│   └── raw/
│       ├── customer_churn_1000_users.csv
│       └── customer_churn_1000_users.xlsx
│
├── notebooks/
│   └── churn_prediction_full.ipynb
│
├── src/
│   ├── churn_model.pkl
│   ├── scaler.pkl
│   └── utils/
│
├── ui/
│   ├── app.py
│   ├── verify_imports.py
│   └── views/
│       ├── dashboard.py
│       └── prediction.py
│
├── venv/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
</pre>

The folder structure consists of the following components:
- `data`: Dataset used for training and testing the model.
- `notebooks`: Jupyter Notebooks used for data exploration and model development.
- `requirements.txt`: List of dependencies required to run the system.
- `src`: Source code for the backend and frontend of the system.
- `ui`: User interface components built using Streamlit.
- `DEPLOYMENT.md`: Deployment instructions for the system.

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DevaSri11/Customer-Churn-prediction.git
   cd Customer-Churn-prediction
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_gsk_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run ui/app.py
   ```
## Live Demo
https://customer-churn-prediction-jbte6cuwjuyeow7uttmwaz.streamlit.app/
