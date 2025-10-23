"""
This script loads the collected solar data, engineers features,
trains a machine learning model, and saves the model to a file
for future predictions.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np

# --- 1. Load the Data ---
# We load the CSV file directly from the repository.
CSV_FILE_PATH = 'solar_data.csv'

print("Loading data from local CSV...")
try:
    df = pd.read_csv(CSV_FILE_PATH)
    if df.empty or len(df) < 50: # Need some data to train
        print(f"Dataset is too small to train (found {len(df)} rows). Waiting for more data.")
        # Exit successfully so the Action doesn't fail
        exit(0) 
    print(f"Data loaded successfully. Found {len(df)} rows.")

    # --- 2. Feature Engineering ---
    print("Engineering features...")
    # Convert timestamp to datetime objects
    df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
    
    # Extract the most important features: the hour and the day
    df['hour'] = df['timestamp_utc'].dt.hour
    df['day_of_year'] = df['timestamp_utc'].dt.dayofyear

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # --- 3. Prepare Data for Model ---
    print("Preparing data for training...")
    features = ['hour', 'day_of_year']
    target = 'solar_radiation_wm2'

    X = df[features]
    y = df[target]

    # Split our data: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 4. Train the Model ---
    print("Training the RandomForest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    
    # Fit the model to our training data
    model.fit(X_train, y_train)
    print("Model training complete.")

    # --- 5. Evaluate the Model ---
    print("Evaluating model performance...")
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Model evaluation complete. Root Mean Squared Error: {rmse:.2f} W/m²")

    # --- 6. Save the Model ---
    model_filename = 'solar_model.joblib'
    joblib.dump(model, model_filename)
    print(f"\nSuccess! Trained model saved as '{model_filename}'.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    # Exit with an error code to make the Action fail
    exit(1)

if __name__ == "__main__":
    pass
