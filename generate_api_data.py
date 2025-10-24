import pandas as pd
import fastf1 as ff1
import openmeteo_requests
import requests_cache
from retry_requests import retry
import os

# --- Setup: Caching is ESSENTIAL for APIs ---

# 1. Setup FastF1 Caching (so you don't re-download GBs of data)
# This will create a 'cache' folder in your project
cache_path = 'cache'
if not os.path.exists(cache_path):
    os.makedirs(cache_path)
ff1.Cache.enable_cache(cache_path)
print(f"FastF1 Caching enabled at: {cache_path}")

# 2. Setup Open-Meteo Caching
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# --- Helper Function for Weather API ---

def fetch_weather(lat, lng, date_str):
    """
    Fetches historical weather for a specific lat/lng/date from Open-Meteo.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": date_str,
        "end_date": date_str,
        "daily": ["temperature_2m_mean", "precipitation_sum"]
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        daily = response.Daily()
        
        return {
            'Temperature': daily.Variables(0).ValuesAsNumpy()[0],
            'RainProbability': 1 if daily.Variables(1).ValuesAsNumpy()[0] > 0.1 else 0 # 1 if > 0.1mm rain
        }
    except Exception as e:
        print(f"Weather API Error for {date_str}: {e}")
        return {'Temperature': None, 'RainProbability': None}

# --- Main Data Generation Function ---

def generate_data():
    print("Loading base data files...")
    # Load the "keys" we need to call the APIs
    races = pd.read_csv('data/races.csv')
    circuits = pd.read_csv('data/circuits.csv')
    drivers = pd.read_csv('data/drivers.csv')

    # Merge races and circuits to get lat/lng for each race
    races_with_circuits = pd.merge(races, circuits, on='circuitId', how='left')
    
    # We'll focus on the modern era for faster processing
    races_to_process = races_with_circuits[races_with_circuits['year'] >= 2014].copy()
    
    all_weather_data = []
    all_pace_data = []

    print(f"Starting to process {len(races_to_process)} races. This will take a long time...")

    for index, race in races_to_process.iterrows():
        print(f"Processing: {race['year']} {race['name_x']}...")
        
        # --- 1. Get Weather Data ---
        weather_info = fetch_weather(race['lat'], race['lng'], race['date'])
        weather_info['raceId'] = race['raceId']
        all_weather_data.append(weather_info)
        
        # --- 2. Get FastF1 Pace Data ---
        try:
            # Load the race session
            session = ff1.get_session(race['year'], race['round'], 'R') # 'R' is for Race
            session.load(laps=True, telemetry=False, weather=False) # We don't need telemetry here

            # Get all laps for all drivers
            laps = session.laps
            
            for driver_abbr in laps['Driver'].unique():
                # Map driver abbreviation (e.g., 'VER') to the driverId (e.g., 830)
                driver_row = drivers[drivers['code'] == driver_abbr]
                if driver_row.empty:
                    continue # Skip if driver (e.g., guest) isn't in our file
                
                driver_id = driver_row.iloc[0]['driverId']
                
                # Use pick_quick() to filter out slow/pit/formation laps. This is a powerful feature!
                driver_laps = laps.pick_driver(driver_abbr).pick_quick()
                
                if not driver_laps.empty:
                    # Calculate median pace from all "clean" laps
                    median_pace = driver_laps['LapTime'].median()
                    
                    all_pace_data.append({
                        'raceId': race['raceId'],
                        'driverId': driver_id,
                        'MedianRacePace': median_pace
                    })

        except Exception as e:
            print(f"  -> Error processing FastF1 data for {race['year']} {race['name_x']}: {e}")

    # --- 3. Save the new data to CSVs ---
    print("Processing complete. Saving new data files...")
    
    weather_df = pd.DataFrame(all_weather_data)
    weather_df.to_csv('data/generated_weather.csv', index=False)
    print("Saved 'data/generated_weather.csv'")
    
  if all_pace_data:
        pace_df = pd.DataFrame(all_pace_data)
        pace_df.to_csv('data/generated_pace.csv', index=False)
        print(f"Saved {len(pace_df)} rows to 'data/generated_pace.csv'")
    else:
        print("Warning: No pace data was generated.")
        # Create a file with just headers so it's not "empty"
        pd.DataFrame(columns=['raceId', 'driverId', 'MedianRacePace']).to_csv('data/generated_pace.csv', index=False)
        print("Created 'data/generated_pace.csv' with headers (no data found).")

if __name__ == "__main__":
    generate_data()