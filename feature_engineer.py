import pandas as pd
import numpy as np

def engineer_features(df):
    """
    Engineers new features based on the raw merged data.
    """
    print("Engineering features...")
    
    # --- Convert Data Types ---
    df['date'] = pd.to_datetime(df['date'])
    df['finalPosition'] = df['positionOrder']
    
    # --- Target Variable (What we want to predict) ---
    df['Winner'] = df['finalPosition'].apply(lambda x: 1 if x == 1 else 0)

    # --- Feature 1: QualifyingTime (s) ---
    df['GridPosition'] = df['grid'].apply(lambda x: 20 if x == 0 else x)
    
    # --- Feature 2: PositionChange ---
    df['PositionChange'] = df['GridPosition'] - df['finalPosition']

    # --- Feature 3 & 4: RainProbability & Temperature (C) ---
    # This data is simulated as it is not in the original dataset.
    print("Warning: Simulating 'Temperature' and 'RainProbability'.")
    np.random.seed(42)
    df['Temperature'] = np.random.uniform(15, 35, len(df))
    df['RainProbability'] = np.random.choice([0, 0.1, 0.5, 0.9], len(df), p=[0.7, 0.15, 0.1, 0.05])

    # --- Feature 5: TeamPerformanceScore (Engineered) ---
    team_points = df.groupby(['raceId', 'constructorId'])['points'].sum().reset_index()
    df = pd.merge(df, team_points.rename(columns={'points': 'teamPointsInRace'}), on=['raceId', 'constructorId'], how='left')
    
    df = df.sort_values(by='date')
    
    df['TeamPerformanceScore'] = df.groupby(['year', 'constructorId'])['teamPointsInRace'].shift(1).rolling(window=5, min_periods=1).mean()
    
    # --- Clean Up Data ---
    df['TeamPerformanceScore'] = df['TeamPerformanceScore'].fillna(0)
    df = df.dropna(subset=['GridPosition'])
    
    print("Feature engineering complete.")
    
    # --- THIS IS THE FIX ---
    return df