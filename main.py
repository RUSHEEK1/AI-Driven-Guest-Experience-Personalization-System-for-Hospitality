import ollama
import pandas as pd
import json

# Initialize the Ollama client
client = ollama.Client()

# Function to analyze sentiment for a single review
def analyze_sentiment_and_analysis(text_data):
    try:
        # Make the API call for sentiment analysis
        response = client.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are a sentiment analysis expert specializing in customer feedback evaluation. "
                        "Your task is to analyze feedback, classify the sentiment as Positive, Negative, or Neutral, "
                        "provide a concise yet detailed explanation for your classification, and recommend specific improvements where applicable.\n\n"

                        "Examples:\n\n"

                        "1. Feedback: 'The hotel staff were friendly, and the amenities were excellent.'\n"
                        "   Sentiment: Positive\n"
                        "   Analysis: The feedback highlights positive experiences with staff and amenities. "
                        "   The use of words like 'friendly' and 'excellent' conveys a strong positive sentiment.\n"
                        "   Improvement: No improvement needed. Maintain the current standards.\n\n"

                        "2. Feedback: 'The room was dirty, and the air conditioning did not work.'\n"
                        "   Sentiment: Negative\n"
                        "   Analysis: The feedback identifies critical issues such as an unclean room and malfunctioning air conditioning. "
                        "   These problems severely impact the guest's experience, leading to a negative sentiment.\n"
                        "   Improvement: Focus on improving room cleanliness and ensuring all air conditioning units are functional.\n\n"

                        "Now analyze the following feedback:\n"
                        f"Feedback: '{text_data}'\n"
                        "Provide the sentiment, a detailed analysis, and actionable suggestions for improvement."
                    )
                }
            ]
        )

        # Extract sentiment and detailed analysis from the response
        if response and 'message' in response:
            content = response['message']['content']

            sentiment = content.split("\n")[0]  # First line is sentiment
            analysis = "\n".join(content.split("\n")[1:]).strip()  # Everything else is analysis

            return sentiment.strip(), analysis
        else:
            return "No response from the model.", "No analysis available."
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Error during analysis.", "No analysis available."

# Dataset loading function (optional, use only when needed)
def load_dataset(dataset_path):
    try:
        dataset = pd.read_csv(dataset_path)
        print("Dataset loaded successfully!")
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Call the analyze_sentiment_and_analysis function
feedback_text = "review"
sentiment, analysis = analyze_sentiment_and_analysis(feedback_text)

# Print the results
print("Sentiment:", sentiment)
print("Analysis:", analysis)
