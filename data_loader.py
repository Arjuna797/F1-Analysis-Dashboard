import pandas as pd
import os

def load_all_data(data_path='data/'):
    """
    Loads and merges all necessary F1 CSV files into a single DataFrame.
    """
    print("Loading datasets...")
    
    # Load all required CSVs
    try:
        races = pd.read_csv(os.path.join(data_path, 'races.csv'))
        results = pd.read_csv(os.path.join(data_path, 'results.csv'))
        qualifying = pd.read_csv(os.path.join(data_path, 'qualifying.csv'))
        constructors = pd.read_csv(os.path.join(data_path, 'constructors.csv'))
        circuits = pd.read_csv(os.path.join(data_path, 'circuits.csv'))
        status = pd.read_csv(os.path.join(data_path, 'status.csv'))
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure all CSV files (races, results, qualifying, constructors, circuits, status) are in the 'data/' folder.")
        return None

    # --- Merging ---
    
    # 1. Merge results with status
    df = pd.merge(results, status, on='statusId', how='left')
    
    # 2. Merge with races 
    df = pd.merge(df, races[['raceId', 'year', 'circuitId', 'date', 'name']].rename(columns={'name': 'raceName'}), on='raceId', how='left')
    
    # 3. Merge with circuits
    df = pd.merge(df, circuits[['circuitId', 'name', 'location', 'country']], on='circuitId', how='left')
    
    # 4. Merge with constructors
    df = pd.merge(df, constructors[['constructorId', 'name', 'nationality']].rename(columns={'name': 'constructorName'}), on='constructorId', how='left')
    
    # 5. Merge with qualifying
    q_simple = qualifying[['raceId', 'driverId', 'position']].rename(columns={'position': 'qualifyingPosition'})
    df = pd.merge(df, q_simple, on=['raceId', 'driverId'], how='left')

    print("Data loading and merging complete.")
    return df