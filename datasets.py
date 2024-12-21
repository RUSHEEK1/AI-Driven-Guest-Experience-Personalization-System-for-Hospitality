import pandas as pd
import random


def copy_columns_to_another_dataset(source_csv, target_csv, columns, output_csv):
    # Load the datasets from the CSV files
    source_df = pd.read_csv(source_csv)  # Dataset to copy the columns from
    target_df = pd.read_csv(target_csv)  # Dataset to paste the columns into
    
    # Copy multiple columns from the source dataframe to the target dataframe
    for column in columns:
        target_df[column] = source_df[column]
    
    # Save the updated target dataframe to a new CSV file
    target_df.to_csv(output_csv, index=False)
    print(f"Columns {columns} have been copied to {output_csv}.")

# Example usage
#copy_columns_to_another_dataset('source_csv','target_csv',['column names'],'target_csv')



def drop_columns_from_dataset(file_path, columns_to_drop, output_path):
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        
        # Check if the columns exist and drop them
        for column in columns_to_drop:
            if column in df.columns:
                df.drop(column, axis=1, inplace=True)
                print(f"Column '{column}' dropped.")
            else:
                print(f"Column '{column}' not found in the DataFrame.")
        
        # Save the updated DataFrame
        df.to_csv(output_path, index=False)
        print(f"Updated dataset saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
#drop_columns_from_dataset(file_path="file.csv",columns_to_drop=['coloumn name'],output_path="file.csv")



def generate_hotel_preferences(num_samples=20492):
    # Define possible values for each column
    food_preferences = ["Vegetarian", "Vegan", "Non-Vegetarian", "Gluten-Free", "Keto", "Pescatarian"]
    room_types_realistic = {
        "Deluxe": 5000,
        "Standard": 10000,
        "Suite": 12500,
        "Economy": 2500
    }
    sports_activities_no_none = ["Tennis", "Swimming", "Golf", "Yoga", "Cycling"]
    wellness_activities_no_none = ["Gym", "Sauna", "Spa", "Hot Tub", "Massage"]

    # Generate data without "None" values
    data_no_none = {
        "FoodPreference": [random.choice(food_preferences) for _ in range(num_samples)],
        "RoomType": [random.choice(list(room_types_realistic.keys())) for _ in range(num_samples)],
        "Price": [],
        "SportsActivity": [random.choice(sports_activities_no_none) for _ in range(num_samples)],
        "WellnessActivity": [random.choice(wellness_activities_no_none) for _ in range(num_samples)],
    }

    # Assign prices based on room type
    for room in data_no_none["RoomType"]:
        data_no_none["Price"].append(room_types_realistic[room])

    # Create a DataFrame
    df_no_none = pd.DataFrame(data_no_none)
    return df_no_none

def save_to_csv(df, filename="hotel_preferences.csv"):
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")

# Generate the dataset
#df = generate_hotel_preferences()

# Save the dataset to a CSV file
#save_to_csv(df, file.csv")




