import pandas as pd

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
copy_columns_to_another_dataset(fr"C:\Users\rushe\OneDrive\Desktop\datasets\hotel_booking.csv",
  fr"C:\Users\rushe\OneDrive\Desktop\datasets\hotel_reviews.csv",
  ['Name', 'email','phone-number','credit_card','arrival_date_month','arrival_date_day_of_month',
  'stays_in_weekend_nights','stays_in_week_nights','adults','children','required_car_parking_spaces',
  'reservation_status'],
  fr"C:\Users\rushe\OneDrive\Desktop\datasets\hotel_reviews.csv")
