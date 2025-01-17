import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import random

data = pd.read_csv(file.csv")  # Replace with the path to your dataset
print(data.head())

RESHAPE THE DATA:

reshaped_data = pd.melt(
    data,
    id_vars=['Name', 'Rating', 'phone-number'],
    value_vars=['FoodPreference', 'WellnessActivity', 'SportsActivity'],
    var_name='category',
    value_name='activities'
)
activities_data = reshaped_data.groupby('category')['activities'].unique().to_dict()


#GENERATE USER DATA:

def generate_user_data(data, num_users=100, num_days=30):
    user_data = []
    start_date = datetime.now() - timedelta(days=num_days)

    # Slice the dataset to only include the first 'num_users' entries
    data_subset = data.head(num_users)

    # Get the required columns only once
    user_info = data_subset[['Name', 'email', 'Price', 'RoomType']].drop_duplicates()

    # Convert the user info to a dictionary for faster access without setting 'Name' as index
    user_dict = user_info.to_dict(orient='records')  # Creating a list of dictionaries

    for user_details in user_dict:
        name = user_details['Name']
        email = user_details['email']
        price = user_details['Price']

        # User preferences (1-5 rating)
        for category, activities in activities_data.items():
            for activity in activities:
                # Not all users will have interactions with all activities
                if random.random() > 0.3:  # 70% chance of having an interaction
                    user_data.append({
                        'name': name,
                        'category': category,
                        'activity': activity,
                        'rating': random.randint(1, 5),
                        'time_spent': random.randint(30, 180),  # minutes
                        'email': email,
                        'price': price,
                        
                    })

    return pd.DataFrame(user_data)

# Call the function with your dataset
user_data_df = generate_user_data(data, num_users=100, num_days=30)
data = generate_user_data(data)
data

BUILD USER PROFILE:

def build_user_profiles(data, user_profiles=None):
    user_profiles = data.pivot_table(
        index='name',
        columns='activity',
        values='rating',
        aggfunc='mean'
    ).fillna(0)

    time_spent_profile = data.pivot_table(
        index='name',
        columns='activity',
        values='time_spent',
        aggfunc='mean'
    ).fillna(0)

    time_spent_profile = time_spent_profile / time_spent_profile.max()

    user_profiles = (user_profiles * 0.7) + (time_spent_profile * 0.3)

    similarity_matrix = cosine_similarity(user_profiles)

    return similarity_matrix, user_profiles

similarity_matrix, user_profiles = build_user_profiles(data)
similarity_matrix

GET SIMILAR USERS:

def get_similar_users(data, user_id, n=5, similarity_matrix=None):
    if similarity_matrix is None:
        similarity_matrix, user_profiles = build_user_profiles(data)
    
    user_idx = user_profiles.index.get_loc(user_id)
    
    user_similarities = similarity_matrix[user_idx]
    
    similar_user_indices = user_similarities.argsort()[::-1][1:n+1]
    
    similar_users = user_profiles.index[similar_user_indices]

    return similar_users

RECOMENDATION:

def get_recommendations(data, name, category=None, n=5):
    similar_users = get_similar_users(data, name)

    similar_users_data = data[data['name'].isin(similar_users)]

    if category:
        similar_users_data = similar_users_data[
            similar_users_data['category'] == category
        ]

    recommendations = similar_users_data.groupby('activity').agg({
        'rating': 'mean',
        'time_spent': 'mean'
    }).sort_values('rating', ascending=False)

    user_activities = set(data[data['name'] ==name]['activity'])
    new_activities = recommendations[~recommendations.index.isin(user_activities)]

    return new_activities.head(n)

new_activities = get_recommendations(data,"USER",category="WellnessActivity")
new_activities

new_activities = get_recommendations(data,"OTHER USER")
new_activities
