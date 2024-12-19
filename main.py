from openai import OpenAI
import pandas as pd

# Set up the OpenAI client for interacting with the Gemini model on OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",  # Use your actual OpenRouter API key
)

# Function to analyze sentiment for each review in the dataset
def analyze_sentiment(text_data):
    completion = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",  # Specify the model for sentiment analysis
        messages=[  # Provide the user's text to analyze sentiment
            {
                "role": "user",
                "content": f"Please analyze the sentiment of the following review: {text_data}"  # Pass the review for analysis
            }
        ]
    )
    # Return the sentiment analysis result
    return completion.choices[0].message.content

# Load your dataset (replace 'your_dataset.csv' with the actual dataset path)
dataset = pd.read_csv(fr"C:\Users\rushe\OneDrive\Desktop\datasets\hotel_reviews.csv")

# Print all column names to check if 'review_column' exists
print(dataset.columns)

# Replace 'review_column' with the actual column name in your dataset
for index, row in dataset.iterrows():
    review_text = row['Review']  # Update 'review_column' with the correct column name
    sentiment_result = analyze_sentiment(review_text)
    print(f"Review: {review_text}\nSentiment: {sentiment_result}\n")
