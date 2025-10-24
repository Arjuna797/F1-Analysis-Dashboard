#!/bin/bash

# This script runs the data generation and then starts the Streamlit app.

DATA_DIR="data"
PACE_FILE="$DATA_DIR/generated_pace.csv"
WEATHER_FILE="$DATA_DIR/generated_weather.csv"

# Check if the generated data files exist. If not, run the generation script.
if [ ! -f "$PACE_FILE" ] || [ ! -f "$WEATHER_FILE" ]; then
    echo "Generated data not found. Running generate_api_data.py..."
    python generate_api_data.py
fi

echo "Starting Streamlit app..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0