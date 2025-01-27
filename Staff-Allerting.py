from slack_sdk.webhook import WebhookClient
from recomendation1 import get_recommendations
from main import analyze_sentiment_and_analysis
import pandas as pd
def send_slack_notification(message, slack_webhook_url):
    """
    Sends a Slack notification with the given message to the specified webhook URL.

    Args:
        message (str): The message to send to Slack.
        slack_webhook_url (str): Slack Webhook URL for sending notifications.

    Raises:
        ValueError: If the Slack Webhook URL is not provided or invalid.
    """
    if not slack_webhook_url or "hooks.slack.com" not in slack_webhook_url:
        raise ValueError("Invalid or missing Slack Webhook URL.")

    try:
        webhook = WebhookClient(slack_webhook_url)
        response = webhook.send(text=message)
        if response.status_code == 200 and response.body == "ok":
            print("Slack notification sent successfully!")
        else:
            print(f"Failed to send Slack notification. Response: {response.body}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")


def generate_slack_message(username, review, sentiment_analysis, recommendation=None):
    """
    Constructs a Slack message with the provided details.

    Args:
        username (str): Username of the reviewer.
        review (str): Review text provided by the user.
        sentiment_analysis (tuple): Sentiment and analysis details.
        recommendation (str, optional): Recommendations generated for the user.

    Returns:
        str: A formatted Slack message.
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

def main():
    """
    Main function to take input, perform sentiment analysis, generate recommendations,
    and send a Slack notification.
    """
    # Replace with your actual Slack Webhook URL
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
        recommendation = None
        try:
            # Call get_recommendations
            recommendation_data = get_recommendations( username, review)

            # Debugging: Print the recommendation data
            print(f"Raw recommendation data: {recommendation_data}")

            # Ensure recommendation_data is a list
            if isinstance(recommendation_data, list):
                recommendation = ", ".join(recommendation_data)  # Combine activities into a single string
            else:
                print("Error in recommendations: Expected a list but got something else.")
                recommendation = "No recommendations available"
        
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            recommendation = "Error while generating recommendations."

        # Generate the Slack message
        slack_message = generate_slack_message(username, review, sentiment_analysis, recommendation)
        
        # Send the Slack notification
        send_slack_notification(slack_message, slack_webhook_url)
    
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"Error in main workflow: {e}")



if __name__ == "__main__":
    main()
