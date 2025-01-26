import pandas as pd

def Cleaning_Data(matches_data, saving_path):
    # Drop the 'umpire3' column
    matches_data_clean = matches_data.drop(columns=["umpire3"])

    # Fill missing values with 'unknown'
    columns_with_missing_data = ['city', 'winner', 'player_of_match', 'umpire1', 'umpire2']
    matches_data_clean[columns_with_missing_data] = matches_data_clean[columns_with_missing_data].fillna("unknown")
    
    # Convert 'date' column to datetime
    matches_data_clean["date"] = pd.to_datetime(matches_data_clean["date"])
    
    # Remove duplicates
    matches_data_clean = matches_data_clean.drop_duplicates()
    
    # Standardize text data
    textual_columns = ['team1', 'team2', 'toss_winner', 'winner', 'venue', 'player_of_match', 'city', 'umpire1', 'umpire2']
    matches_data_clean[textual_columns] = matches_data_clean[textual_columns].apply(lambda col: col.str.strip().str.title())

    # Print outliers
    outliers = matches_data_clean[(matches_data_clean['win_by_runs'] < 0) | (matches_data_clean['win_by_wickets'] < 0)]
    if not outliers.empty:
        print("Following are the outliers of the dataset:")
        print(outliers)

    # Add derived column 'match_outcome'
    matches_data_clean['match_outcome'] = matches_data_clean.apply(
        lambda row: 'Target is defended' if row['win_by_runs'] > 0 else 
                    ('Target is chased' if row['win_by_wickets'] > 0 else 'Tie/No Result'), axis=1
    )

    # Ensure 'dl_applied' is binary
    matches_data_clean['dl_applied'] = matches_data_clean['dl_applied'].apply(lambda x: 1 if x == 1 else 0)

    # Save cleaned dataset
    matches_data_clean.to_csv(saving_path, index=False)
    print(f"Cleaned dataset saved to {saving_path}")

if __name__ == "__main__":
        # Prompt user for file paths
    print("Enter the path of your dataset you want to clean:")
    file_path = input().strip()
    print("Enter the .csv path where you want to save the cleaned data:")
    saving_path = input().strip()
        
        # Load and clean the data
    matches_data = pd.read_csv(file_path)
    print("Original Dataset Info:")
    print(matches_data.info())
    print(matches_data.head())
    Cleaning_Data(matches_data, saving_path)
    
    
