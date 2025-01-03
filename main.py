import ollama
import pandas as pd
import json

# Initialize the Ollama client
client = ollama.Client()

# Function to analyze sentiment for each review in the dataset
def analyze_sentiment_and_analysis(text_data):
    try:
        # Make the API call for sentiment analysis
        response = client.chat(
            model="llama3.2",  # model name/version for Ollama
            messages=[
                {
                    "role": "user",
                    "content": (

                    "You are a sentiment analysis expert specializing in customer feedback evaluation. "
                    "Your task is to analyze feedback, classify the sentiment as Positive, Negative, or Neutral, "
                    "provide a concise yet detailed explanation for your classification, and recommend specific improvements where applicable. "
                    "Your goal is to help improve customer satisfaction by identifying areas of concern and excellence.\n\n"

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
            
            # Get the first line as sentiment
            sentiment = content.split("\n")[0]  # Get the first line, which is the sentiment
            
            # The remaining part of the response is the analysis
            analysis = "\n".join(content.split("\n")[1:]).strip()  # Get everything except the first line
            
            return sentiment.strip(), analysis
        else:
            return "No response from the model.", "No analysis available."
    except Exception as e:
        # Handle errors gracefully
        print(f"Error analyzing sentiment: {e}")
        return "Error during analysis.", "No analysis available."

# Load your dataset (replace with your actual dataset path)
dataset_path = "file.csv"
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

# Analyze sentiment and analysis for each review and save results
results = []
for index, row in dataset.iterrows():
    review_text = row[review_column]
    print(f"Processing review {index + 1}/{len(dataset)}...")
    
    sentiment_result, analysis_result = analyze_sentiment_and_analysis(review_text)
    
    # Organize the output in the desired format
    results.append({
        "Review": review_text,
        "Analysis": analysis_result,
        "Sentiment": sentiment_result
    })
    
    # Print the formatted output
    print(f"Review:\n{review_text}")
    print(f"Analysis:\n{analysis_result}")
    print(f"Sentiment:\n{sentiment_result}\n")

# Save results to a new JSON file
output_path = "file.json"
try:
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)
    print(f"Sentiment analysis results saved to {output_path}.")
except Exception as e:
    print(f"Error saving results to JSON: {e}")
