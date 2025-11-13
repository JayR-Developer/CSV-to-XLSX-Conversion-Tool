import os
import time
import pandas as pd
import shutil
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file (optional if you want environment fallback)
load_dotenv()

# Streamlit interface
st.title("CSV to XLSX Conversion Tool")

# Get local directory (where the script is running)
local_directory = os.getcwd()

# Inputs for user directory
user_csv_folder = st.text_input('Enter the CSV Folder (relative to your local directory)', value='')
user_output_folder = st.text_input('Enter the Output Folder (relative to your local directory)', value='')

# Set dynamic CSV folder and output folder based on user input
if user_csv_folder:
    csv_folder = os.path.join(local_directory, user_csv_folder)
else:
    # Default to local directory if user doesn't specify
    csv_folder = local_directory

if user_output_folder:
    output_folder = os.path.join(local_directory, user_output_folder)
else:
    # Default to local directory if user doesn't specify
    output_folder = local_directory

# Get full paths of all CSV files in the csv_folder
if os.path.exists(csv_folder):
    files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if os.path.isfile(os.path.join(csv_folder, f)) and f.lower().endswith('.csv')]
else:
    files = []

# Sort by modification time (newest first)
files.sort(key=os.path.getmtime, reverse=True)

# Display the files found in the folder
if files:
    st.write("Files to process:")
    for file in files:
        st.write(f"- {os.path.basename(file)}")
else:
    st.warning("No CSV files found in the specified folder.")

# Button to start processing
if st.button("Process Files"):
    if not csv_folder or not output_folder:
        st.error("Please provide both CSV folder and output folder paths.")
    else:
        start_time = time.time()  # Start the timer

        # Check if there are files to process
        if files:
            processed_files = []
            for csv_fullpath in files:
                # Get filename only (no folder)
                filename = os.path.basename(csv_fullpath)

                # Read the CSV file    
                try:
                    df = pd.read_csv(csv_fullpath, delimiter='|', header=None, encoding='utf-8', low_memory=False, on_bad_lines='warn')

                    # Replace .CSV with .xlsx (case-insensitive safe method)
                    xlsx_filename = os.path.splitext(filename)[0] + ".xlsx"

                    # Build the new output path
                    output_file = os.path.join(output_folder, xlsx_filename)

                    # Convert to Excel and save
                    df.to_excel(output_file, index=False)

                    processed_files.append(f"Done: {filename} ✅")
                except Exception as e:
                    processed_files.append(f"Error processing {filename}: {str(e)}")

            # Display processed files
            for result in processed_files:
                st.write(result)

        else:
            st.warning("No CSV files found in the specified folder.")

        # Log processing time
        end_time = time.time()  # End the timer
        duration = end_time - start_time
        st.write(f"Script completed in {duration:.2f} seconds.")
