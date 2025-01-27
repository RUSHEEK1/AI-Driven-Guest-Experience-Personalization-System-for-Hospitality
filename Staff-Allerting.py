import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from slack_sdk.webhook import WebhookClient
from recomendation1 import get_recommendations
from main import analyze_sentiment_and_analysis

# SMTP server details
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_user = "rusheekgiri@gmail.com"  # Your email
email_password = "xdeu bctu fcug laoi"  # Use an app password for security

def send_email_notification(to_email, subject, body):
    """
    Sends an email notification with the given subject and body to the specified recipient email address.

    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject.
        body (str): Email body text.

    Returns:
        None: Prints success or failure message.
    """
    try:
        # Create an email message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))  # Attach the plain-text body

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade connection to a secure encrypted SSL/TLS connection
            server.login(email_user, email_password)  # Login with your email credentials
            server.send_message(msg)  # Send the email

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def send_slack_notification(slack_webhook_url, message):
    """
    Sends a Slack notification with the given message to the specified webhook URL.

    Args:
        slack_webhook_url (str): Slack Webhook URL for sending notifications.
        message (str): Message to send to Slack.
        
    Returns:
        None: Prints success or failure message.
    """
    try:
        webhook = WebhookClient(slack_webhook_url)
        response = webhook.send(text=message)
        if response.status_code == 200 and response.body == "ok":
            print("Slack notification sent successfully!")
        else:
            print(f"Failed to send Slack notification. Response: {response.body}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")

def generate_message(username, review, sentiment_analysis, recommendation=None):
    """
    Constructs a message for either Slack or email.

    Args:
        username (str): Username of the reviewer.
        review (str): Review text provided by the user.
        sentiment_analysis (tuple): Sentiment and analysis details.
        recommendation (str, optional): Recommendations generated for the user.

    Returns:
        str: A formatted message.
    """
    sentiment, analysis = sentiment_analysis
    message = f"""
    *:warning: Review Notification :warning:*
    - *Username:* {username}
    - *Review:* {review}
    - *{sentiment}*
    - *{analysis}*
    """
    if recommendation:
        message += f"\n    - *Recommendation:* {recommendation}"
    return message.strip()

def get_recommendations_for_review(username, review):
    """
    Get recommendations based on the review and username.

    Args:
        username (str): Username of the reviewer.
        review (str): Review text provided by the user.

    Returns:
        str: Recommendations for the user.
    """
    try:
        recommendation_data = get_recommendations(username, review)
        print(f"Raw recommendation data: {recommendation_data}")

        if isinstance(recommendation_data, list):
            return ", ".join(recommendation_data)  # Combine activities into a single string
        else:
            print("Error in recommendations: Expected a list but got something else.")
            return "No recommendations available"
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return "Error while generating recommendations."

def main():
    """
    Main function to take input, perform sentiment analysis, generate recommendations,
    and send Slack notification and email.
    """
    slack_webhook_url = "https://hooks.slack.com/services/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"

    try:
        # Input user details and review
        username = input("Enter username: ").strip()
        review = input("Enter review: ").strip()

        if not username or not review:
            print("Username and review cannot be empty. Please provide valid inputs.")
            return

        # Perform sentiment analysis
        sentiment_analysis = analyze_sentiment_and_analysis(review)
        
        # Generate recommendations
        recommendation = get_recommendations_for_review(username, review)

        # Generate the message for both Slack and Email
        message = generate_message(username, review, sentiment_analysis, recommendation)

        # Send Slack notification
        send_slack_notification(slack_webhook_url, message)
        
        # Send the same message via email
        subject = "Review Notification"
        send_email_notification("rusheek153@gmail.com", subject, message)
    
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"Error in main workflow: {e}")

if __name__ == "__main__":
    main()
