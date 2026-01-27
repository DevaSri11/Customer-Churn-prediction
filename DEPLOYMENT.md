# Deployment Guide: Streamlit Cloud

Follow these steps to deploy your Customer Churn Prediction app:

## 1. Prepare Your Repository
1. Create a new repository on [GitHub](https://github.com/new).
2. Initialize git in your project folder (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initialize churn prediction app"
   ```
3. Push your code to GitHub:
   ```bash
   git remote add origin https://github.com/DevaSri11/Customer-Churn-prediction.git
   git branch -M main
   git push -u origin main
   ```

## 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select your GitHub repository, branch (`main`), and the main file path: `ui/app.py`.
4. Click **"Deploy!"**.

## 3. Set Up API Keys (Secrets)
Since `.env` files are not pushed to GitHub (for security), you must set them in Streamlit's dashboard:
1. In your app's dashboard on Streamlit Cloud, go to **Settings** > **Secrets**.
2. Add your Groq API key in the following format:
   ```toml
   GROQ_API_KEY = "your_gsk_key_here"
   ```
3. Save. The app will automatically restart and use the key.

> [!IMPORTANT]
> Make sure your `requirements.txt` is up to date in the repository so Streamlit knows which packages to install.
