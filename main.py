from data_loader import load_all_data
from feature_engineer import engineer_features
from model_trainer import train_model
from all_visuals import show_all_visualizations

def main():
    # Step 1: Load and merge all CSVs
    master_df = load_all_data(data_path='data/')
    
    if master_df is None:
        return

    # Step 2: Create all the custom features
    features_df = engineer_features(master_df)

    # Step 3: Train model and get feature importances
    model_data_df, importance_df = train_model(features_df)
    
    if model_data_df is None:
        print("Model training failed. Exiting.")
        return

    print("\n--- Feature Importance Results ---")
    print(importance_df)

    # Step 4: Call the one master function to show all 6 plots in sequence
    show_all_visualizations(
        model_data_df=model_data_df,
        full_features_df=features_df,
        importance_df=importance_df
    )
    
    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()