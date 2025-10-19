"""
This script fetches the latest solar radiation data for London, UK,
and saves it to a CSV file. It is designed to be run once per execution.
"""

import requests
import pandas as pd
from datetime import datetime
import os

CSV_FILE_PATH = 'solar_data.csv'

def collect_solar_data():
    """
    Connects to the Open-Meteo API, fetches the latest solar radiation reading,
    and appends it to a CSV file.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching latest solar radiation data for London...")

    try:
        latitude = 51.5074
        longitude = -0.1278
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=shortwave_radiation"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        current_data = data.get('current', {})
        
        if current_data:
            new_data = pd.DataFrame([{
                'timestamp_utc': current_data.get('time'),
                'solar_radiation_wm2': current_data.get('shortwave_radiation')
            }])

            if os.path.exists(CSV_FILE_PATH):
                new_data.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
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
    collect_solar_data()
    # The script now ends here, allowing the GitHub Action to proceed.


