"""
This script runs continuously to collect solar radiation data for London, UK,
every hour and saves it to a CSV file for future analysis.
"""

import requests
import pandas as pd
from datetime import datetime
import time
import os

CSV_FILE_PATH = 'solar_data.csv'

def collect_solar_data():
    """
    Connects to the Open-Meteo API, fetches the latest solar radiation reading,
    and appends it to a CSV file.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching latest solar radiation data for London...")

    try:
        # Define the coordinates for London.
        latitude = 51.5074
        longitude = -0.1278

        # This is the stable Open-Meteo API endpoint.
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=shortwave_radiation"

        # Make the request to the API.
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response.
        data = response.json()
        current_data = data.get('current', {})
        
        if current_data:
            # Create a DataFrame with the new data point.
            new_data = pd.DataFrame([{
                'timestamp_utc': current_data.get('time'),
                'solar_radiation_wm2': current_data.get('shortwave_radiation')
            }])

            # If the CSV file already exists, append the new data without the header.
            if os.path.exists(CSV_FILE_PATH):
                new_data.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
            # If it's the first time, create the file with the header.
            else:
                new_data.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
            
            print(f"  > Successfully saved data point. Radiation: {current_data.get('shortwave_radiation')} W/m²")
        else:
            print("  > Error: Received empty or invalid data from the API.")

    except requests.exceptions.RequestException as e:
        print(f"  > Error: Failed to retrieve data from the API. Details: {e}")
    except Exception as e:
        print(f"  > Error: An unexpected error occurred. Details: {e}")


if __name__ == "__main__":
    # This loop will run indefinitely.
    while True:
        collect_solar_data()
        # Wait for 1 hour (3600 seconds) before the next collection.
        print(f"  > Waiting for 1 hour...")
        time.sleep(3600)

