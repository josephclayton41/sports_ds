import pandas as pd
import glob
import os

# Set the directory path and team details
directory_path = '/Users/joseph/Documents/Diamondbacks'
team = "Diamondbacks"
years = "21-24"

# Columns to keep (excluding 'Unnamed: 2')
columns_to_keep = ['Gm#', 'Date', 'W/L', 'W-L', 'Rank', 'GB', 'D/N', 'Attendance', 'cLI', 'Streak', 'Orig. Scheduled']

# Get all CSV files in the directory
csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
all_df = []

if not csv_files:
    print("No CSV files found in the specified directory.")
else:
    print(f"Found {len(csv_files)} CSV files.")

# Filter the columns and rows and save them back to the CSV files
for file in csv_files:
    try:
        df = pd.read_csv(file)  # Read the CSV file
        
        # Check if 'Unnamed: 2' exists in the columns
        if 'Unnamed: 2' in df.columns:
            # Step 1: Remove rows where 'Unnamed: 2' column has a value (not null)
            df = df[df['Unnamed: 2'].isnull()]
            print(f"Filtering 'Unnamed: 2' for {file}.")
        else:
            print(f"Warning: 'Unnamed: 2' not found in {file}. Skipping filtering for this column.")
        
        # Step 2: Keep only the specified columns
        df_filtered = df[columns_to_keep]
        
        # Step 3: Drop the 'Unnamed: 2' column if it exists
        if 'Unnamed: 2' in df_filtered.columns:
            df_filtered = df_filtered.drop(columns=['Unnamed: 2'])
        
        # Step 4: Modify 'Streak' column values
        def convert_streak(streak):
            if isinstance(streak, str):
                # Count the number of '+' or '-' characters
                if '+' in streak:
                    return f"{len(streak)}W"
                elif '-' in streak:
                    return f"{len(streak)}L"
            return streak
        
        # Apply the streak conversion function to the 'Streak' column
        df_filtered['Streak'] = df_filtered['Streak'].apply(convert_streak)

        # Check if the filtered DataFrame is empty
        if df_filtered.empty:
            print(f"Warning: The file {file} has no data after filtering.")
        else:
            # Save the modified DataFrame back to the same CSV file
            df_filtered.to_csv(file, index=False)
            # Append the filtered DataFrame to the list
            all_df.append(df_filtered)
            print(f"Processed {file}.")
    
    except Exception as e:
        print(f"Error processing {file}: {e}")  # Handle any errors in reading or writing the file

# Check if there are DataFrames to concatenate
if all_df:
    # Combine all DataFrames into one
    combined_df = pd.concat(all_df, ignore_index=True)

    # Save the combined DataFrame into a new CSV file
    combined_df.to_csv(f"{team}_{years}.csv", index=False)
    print(f"CSV files have been successfully processed and combined into '{team}_{years}.csv'.")
else:
    print("No data was processed, so no files were combined.")
