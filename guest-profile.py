import sqlite3
import json
import pandas as pd

# Load your dataset from a CSV file (replace with your actual file path)
dataset = pd.read_csv('file.csv')

# Connect to the SQLite database
conn = sqlite3.connect("guest_profiles.db")
cursor = conn.cursor()

# Drop the existing table if it exists (to avoid schema issues)
cursor.execute("DROP TABLE IF EXISTS guest_profiles")

# Create table with 19 columns based on your dataset (check this carefully)
cursor.execute("""
CREATE TABLE IF NOT EXISTS guest_profiles (
    review TEXT,
    rating INTEGER,
    name TEXT,
    email TEXT PRIMARY KEY,
    phone_number TEXT,
    credit_card TEXT,
    arrival_date_month TEXT,
    arrival_date_day_of_month INTEGER,
    stays_in_weekend_nights INTEGER,
    stays_in_week_nights INTEGER,
    adults INTEGER,
    children INTEGER,
    required_car_parking_spaces INTEGER,
    reservation_status TEXT,
    room_type TEXT,
    price INTEGER,
    sports_activity TEXT,
    wellness_activity TEXT,
    food_preference TEXT,
    interaction_history TEXT
)
""")

# Iterate through the dataset and insert each row into the table
for _, row in dataset.iterrows():
    # Convert the row to a tuple, ensuring to turn the interaction history into a JSON string
    sample_profile = (
        row['Review'], row['Rating'], row['Name'], row['email'], row['phone-number'],
        row['credit_card'], row['arrival_date_month'], row['arrival_date_day_of_month'],
        row['stays_in_weekend_nights'], row['stays_in_week_nights'], row['adults'],
        row['children'], row['required_car_parking_spaces'], row['reservation_status'],
        row['RoomType'], row['Price'], row['SportsActivity'], row['WellnessActivity'],
        row['FoodPreference'], '[]'  # Assuming interaction history is initially empty
    )

    # Insert the profile data into the database
    cursor.execute("""
    INSERT OR IGNORE INTO guest_profiles (
        review, rating, name, email, phone_number, credit_card, arrival_date_month, arrival_date_day_of_month,
        stays_in_weekend_nights, stays_in_week_nights, adults, children, required_car_parking_spaces, 
        reservation_status, room_type, price, sports_activity, wellness_activity, food_preference, interaction_history
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_profile)

# Commit the changes
conn.commit()

# Check if data was inserted correctly
cursor.execute("SELECT * FROM guest_profiles")
print(cursor.fetchall())

# Example: Fetch interaction history for a specific guest (replace with actual email)
cursor.execute("SELECT interaction_history FROM guest_profiles WHERE email = ?", ("Ernest.Barnes31@outlook.com",))
result = cursor.fetchone()

# Process the interaction history
if result:
    interaction_history = json.loads(result[0])  # Convert JSON string to Python list
else:
    interaction_history = []

print("Current Interaction History:", interaction_history)

# New interaction (e.g., purchase)
new_interaction = {"type": "purchase", "item": "Spa Package", "timestamp": "2025-01-05"}
interaction_history.append(new_interaction)

# Update the interaction history in the database
updated_history = json.dumps(interaction_history)
cursor.execute("""
    UPDATE guest_profiles
    SET interaction_history = ?
    WHERE email = ?
""", (updated_history, "Ernest.Barnes31@outlook.com"))

conn.commit()

# Fetch and print updated interaction history
cursor.execute("SELECT interaction_history FROM guest_profiles WHERE email = ?", ("Ernest.Barnes31@outlook.com",))
print("Updated Interaction History:", json.loads(cursor.fetchone()[0]))

# Close the database connection
conn.close()

