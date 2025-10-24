import streamlit as st
import pandas as pd
from data_loader import load_all_data
from feature_engineer import engineer_features
from model_trainer import train_model
from all_visuals import (
    plot_feature_importance,
    plot_3d_scatter,
    plot_grid_distribution,
    plot_winner_profiles_violin,
    plot_grid_vs_performance_2d_scatter,
    plot_rain_impact_swarm
)

# --- Page Configuration ---
st.set_page_config(
    page_title="F1 Race Analysis Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Caching ---
# Use Streamlit's caching to load and process data only once.
@st.cache_data
def load_and_prepare_data():
    """
    Loads, merges, and engineers all features.
    This function will only run once and its result will be stored.
    """
    master_df = load_all_data(data_path='data/')
    if master_df is None:
        return None, None, None
    
    features_df = engineer_features(master_df)
    model_data_df, importance_df = train_model(features_df)
    
    return features_df, model_data_df, importance_df

# --- Main Application ---
def main():
    # --- Sidebar ---
    st.sidebar.title("About")
    st.sidebar.info(
        "This dashboard analyzes Formula 1 race data to uncover the key factors that contribute to winning a race. "
        "Select a track from the dropdown below to see specific stats and visualizations."
    )
    st.sidebar.title("Data Source")
    st.sidebar.info("Data is sourced from the Ergast API, Kaggle, and supplemented with simulated weather data for this demonstration.")

    # --- Header ---
    st.title("🏎️ Formula 1 Race Winner Analysis")
    st.markdown("An interactive dashboard to explore what it takes to win in F1.")

    # --- Load Data ---
    # Show a spinner while the data is loading for the first time
    with st.spinner('Loading and analyzing historical F1 data... Please wait.'):
        full_features_df, model_data_df, importance_df = load_and_prepare_data()

    if model_data_df is None:
        st.error("Failed to load or process data. Please check your data files and scripts.")
        return

    # --- Track Selector ---
    st.header("Track-Specific Analysis")
    
    # Use 'raceName' for the dropdown
    track_list = sorted(model_data_df['raceName'].unique())
    selected_track = st.selectbox(
        'Select a Grand Prix to analyze:',
        track_list,
        index=track_list.index("Italian Grand Prix") # A good default
    )
    
    track_data = model_data_df[model_data_df['raceName'] == selected_track]

    # --- Key Stats Display ---
    if not track_data.empty:
        # Calculate stats for the selected track
        avg_grid_winner = track_data[track_data['Winner'] == 1]['GridPosition'].mean()
        total_races = track_data['year'].nunique()
        pole_to_win_races = track_data[(track_data['GridPosition'] == 1) & (track_data['Winner'] == 1)]
        pole_win_percentage = (len(pole_to_win_races) / total_races) * 100 if total_races > 0 else 0
        
        # Display stats in columns for a clean look
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Races Analyzed (2014+)", value=total_races)
        with col2:
            st.metric(label="Average Winner's Start Position", value=f"{avg_grid_winner:.2f}")
        with col3:
            st.metric(label="Pole to Win Conversion", value=f"{pole_win_percentage:.1f}%")

    else:
        st.warning("No data available for the selected track in the modern era (2014+).")

    st.markdown("---")

    # --- Graph Display Button ---
    st.header("Overall Analysis Graphs")
    st.info("Click the button below to display the full analysis across all tracks.")

    if st.button('Show Full Analysis Graphs', type="primary"):
        with st.spinner("Generating graphs..."):
            
            # --- Feature Importance ---
            st.subheader("1. Which Factor is Most Important for Winning?")
            fig = plot_feature_importance(importance_df)
            st.pyplot(fig)
            st.markdown(
                """
                **Interpretation:** This chart shows the 'importance score' our machine learning model assigned to each factor. 
                A higher score means the factor was more decisive in predicting a race winner. As we can see, **Grid Position** and **Team Performance** are overwhelmingly the most critical factors.
                """
            )
            st.markdown("---")

            # --- 2D Scatter ---
            st.subheader("2. The 'Winning Zone': Grid Position vs. Team Performance")
            fig = plot_grid_vs_performance_2d_scatter(model_data_df)
            st.pyplot(fig)
            st.markdown(
                """
                **Interpretation:** Each dot represents a driver in a race. The gold dots (Winners) are almost exclusively located in the **top-left corner**, 
                proving that to win a race, you almost always need to start at the front (`Grid Position` < 10) in a top-performing car (`TeamPerformanceScore` > 10).
                """
            )
            st.markdown("---")
            
            # --- Violin Plots ---
            st.subheader("3. How Winners Differ from the Rest of the Field")
            fig = plot_winner_profiles_violin(model_data_df)
            st.pyplot(fig)
            st.markdown(
                """
                **Interpretation:** These plots compare the distribution for Winners vs. Non-Winners.
                - **Team Performance:** The 'Winner' violin is high and narrow, showing winners consistently come from high-performing teams.
                - **Grid Position:** The 'Winner' violin is clustered at the top, confirming they start at the front.
                - **Position Change:** Both violins are centered around zero, indicating that most drivers, including winners, tend to finish close to where they started.
                """
            )
            st.markdown("---")

            # --- 3D Scatter ---
            st.subheader("4. 3D Analysis of Key Factors")
            fig = plot_3d_scatter(model_data_df)
            st.pyplot(fig)
            st.markdown(
                """
                **Interpretation:** This 3D plot combines the three most important factors. You can see the gold "Winner" dots clustered in a specific zone: 
                high Team Performance, low Grid Position, and a Position Change near zero.
                """
            )


if __name__ == '__main__':
    main()
