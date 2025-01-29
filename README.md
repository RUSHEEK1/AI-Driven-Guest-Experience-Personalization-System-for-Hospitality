# AI-Driven Guest Experience Personalization System for Hospitality

## Overview
This repository contains the work done during my internship at Infosys, where I developed an AI-driven guest experience personalization system for the hospitality industry. The project leverages Large Language Models (LLMs) like OpenAI GPT and Meta LLAMA for sentiment analysis and integrates with Mock CRM data through Google Sheets and User Emails. The goal is to enhance guest satisfaction by providing personalized recommendations and proactive service adjustments.

## Features
- **Sentiment Analysis**: Extracts insights from guest reviews and feedback.
- **Personalized Recommendations**: Suggests activities and services based on guest preferences.
- **Integration with Mock CRM Data**: Fetches and updates guest details in Google Sheets.
- **Email-Based Communication**: Automates guest interaction through personalized emails.
- **Data Categorization**: Merges `SportsActivity`, `FoodPreference`, and `WellnessActivity` into a single `category` column for better recommendations.

## Tech Stack
- **Programming Language**: Python
- **Libraries & Frameworks**: OpenAI API, Pandas, NumPy, Ollama
- **Data Storage**: Google Sheets/ Excel sheets(via API integration)
- **Sentiment Analysis**: OpenAI GPT, Meta LLAMA
- **Deployment**: Local/Cloud environment

## Dataset
The dataset includes the following columns:
- Review, Rating, Name, Email, Phone Number, Credit Card Details (mocked), Arrival Date, Stay Duration, Required Car Parking, Reservation Status, Room Type, Price, Sports Activity, Wellness Activity, Food Preference.

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-guest-experience.git
   cd ai-guest-experience
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Google Sheets API and OpenAI API keys.
5. Run the main script:
   ```bash
   python main.py
   ```

## Usage
- Run the script to fetch guest data and perform sentiment analysis.
- Generate personalized recommendations based on the analysis.
- Automate email communication for better guest engagement.

## Future Enhancements
- Implement real-time feedback analysis.
- Improve recommendation accuracy with fine-tuned LLM models.
- Enhance automation for better CRM integration.

## Author
**[Your Name]**

## License
This project is licensed under the MIT License.

## Acknowledgments
- Infosys for providing mentorship and guidance.
- OpenAI and Meta for AI models.
- Google Sheets API for data management.

---
Feel free to fork, contribute, and enhance the project!

