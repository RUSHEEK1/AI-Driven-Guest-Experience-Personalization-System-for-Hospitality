import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from slack_sdk.webhook import WebhookClient
from recomendation1 import get_recommendations
from main import analyze_sentiment_and_analysis
import pandas as pd

# SMTP server details
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_user = "email.com"  # Your email
email_password = "password"  # Use an app password for security

def send_email_notification(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)

        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email notification: {e}")

def send_slack_notification(slack_webhook_url, message):
    try:
        webhook = WebhookClient(slack_webhook_url)
        response = webhook.send(text=message)
        if response.status_code == 200 and response.body == "ok":
            st.success("Slack notification sent successfully!")
        else:
            st.error(f"Failed to send Slack notification. Response: {response.body}")
    except Exception as e:
        st.error(f"Error sending Slack notification: {e}")

def generate_message(username, review, sentiment_analysis, recommendation=None):
    sentiment, analysis = sentiment_analysis
    message = f"""
    *:WARNING: Review Notification :WARNING:*
    - Username: {username}
    - Review: {review}
    - {sentiment}
    - {analysis}
    """
    if recommendation:
        message += f"\n    - *Recommendation:* {recommendation}"
    return message.strip()


# Load the dataset
dataset_path = "file.csv"
try:
    data = pd.read_csv(dataset_path)  # Ensure dataset is available
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    data = None

def get_recommendations_for_review(username, review):
    try:
        if data is None or data.empty:
            return "No data available for recommendations."

        # Ensure a valid category is provided
        category = "SportsActivity"  # Change this based on user preferences

        # Call get_recommendations with the correct arguments
        recommendation_data = get_recommendations(data, username, category)

        if isinstance(recommendation_data, list):
            return ", ".join(recommendation_data)
        else:
            return "No recommendations available"

    except Exception as e:
        return f"Error while generating recommendations: {str(e)}"


st.title("Review Sentiment Analysis & Notification System")

# Set the constant Slack Webhook URL
slack_webhook_url = "url"  # Replace with your actual Slack Webhook URL

username = st.text_input("Enter Username:")
review = st.text_area("Enter Review:")

if st.button("Analyze & Notify"):
    if username and review:
        sentiment_analysis = analyze_sentiment_and_analysis(review)
        recommendation = get_recommendations_for_review(username, review)
        message = generate_message(username, review, sentiment_analysis, recommendation)
        send_slack_notification(slack_webhook_url, message)
        send_email_notification("rusheek153@gmail.com", "Review Notification", message)
    else:
        st.error("Please enter both Username and Review before proceeding.")

