from openai import OpenAI
import pandas as pd

# Set up the OpenAI client for interacting with the Gemini model on OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="API KEY"  # Replace with an environment variable for security
)

# Function to analyze sentiment for each review in the dataset
def analyze_sentiment(text_data):
    try:
        # Make the API call for sentiment analysis
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",  # Check model availability
            messages=[
                {
                    "role": "user",
                    "content": f"Please analyze the sentiment of the following review: {text_data}"
                }
            ]
        )
        # Safely return the sentiment analysis result
        if completion and completion.choices:
            return completion.choices[0].message.content
        else:
            return "No response from the model."
    except Exception as e:
        # Handle errors gracefully
        print(f"Error analyzing sentiment: {e}")
        return "Error during analysis."

# Load your dataset (replace with your actual dataset path)
dataset_path = "data.csv"
try:
    dataset = pd.read_csv(dataset_path)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Check the dataset columns
print("Dataset Columns:", dataset.columns)

# Replace 'Review' with the actual column name for reviews in your dataset
review_column = 'Review'  # Update this to match your dataset's structure

# Verify the review column exists
if review_column not in dataset.columns:
    print(f"Error: Column '{review_column}' not found in the dataset.")
    exit()

# Analyze sentiment for each review and save results
results = []
for index, row in dataset.iterrows():
    review_text = row[review_column]
    print(f"Processing review {index + 1}/{len(dataset)}...")
    sentiment_result = analyze_sentiment(review_text)
    results.append({"Review": review_text, "Sentiment": sentiment_result})
    print(f"Review: {review_text}\nSentiment: {sentiment_result}\n")

# Save results to a new CSV file
output_path = "file.csv"
results_df = pd.DataFrame(results)
results_df.to_csv(output_path, index=False)
print(f"Sentiment analysis results saved to {output_path}.")

# Replace 'review_column' with the actual column name in your dataset
for index, row in dataset.iterrows():
    review_text = row['Review']  # Update 'review_column' with the correct column name
    sentiment_result = analyze_sentiment(review_text)
    print(f"Review: {review_text}\nSentiment: {sentiment_result}\n")
