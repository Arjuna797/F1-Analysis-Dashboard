import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd  # <-- FIX 1: This line was missing

def plot_feature_importance(importance_df):
    """
    Creates a bar chart of the most important features.
    """
    print("Displaying Feature Importance plot...")
    plt.figure(figsize=(10, 6))
    
    # --- FIX 2: Updated this line to fix the warning ---
    sns.barplot(x='importance', y='feature', data=importance_df, hue='feature', palette='viridis', legend=False)
    # ---
    
    plt.title('Which Factor Decides the Race Winner?', fontsize=16)
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    plt.show()

def plot_3d_scatter(df):
    """
    Creates the 3D scatter plot as requested.
    """
    print("Displaying 3D Winner Analysis plot...")
    
    # We'll sample the data to make the 3D plot clearer
    # All winners, and a random 10% sample of non-winners
    winners = df[df['Winner'] == 1]
    non_winners = df[df['Winner'] == 0].sample(frac=0.1, random_state=42)
    
    # This line will now work because 'pd' is imported
    plot_df = pd.concat([winners, non_winners])
    
    # Map colors
    colors = plot_df['Winner'].map({1: 'gold', 0: 'blue'})
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create the 3D scatter plot
    ax.scatter(
        plot_df['GridPosition'], 
        plot_df['TeamPerformanceScore'], 
        plot_df['PositionChange'], 
        c=colors, 
        s=20,  # size
        alpha=0.6
    )
    
    ax.set_title('3D Analysis of Race Winners', fontsize=16)
    ax.set_xlabel('Grid Position (Lower is better)')
    ax.set_ylabel('Team Performance Score')
    ax.set_zlabel('Positions Gained/Lost')
    
    # Create a legend
    gold_patch = plt.Line2D([0], [0], marker='o', color='w', label='Winner', markersize=10, markerfacecolor='gold')
    blue_patch = plt.Line2D([0], [0], marker='o', color='w', label='Non-Winner', markersize=10, markerfacecolor='blue')
    ax.legend(handles=[gold_patch, blue_patch])
    
    # Invert X-axis so P1 is in the "front"
    ax.invert_xaxis()
    
    plt.show()

def plot_grid_distribution(df):
    """
    Shows the distribution of starting positions for winners vs. non-winners.
    """
    print("Displaying Grid Position plot...")
    plt.figure(figsize=(12, 7))
    sns.kdeplot(df[df['Winner'] == 0]['GridPosition'], label='Non-Winner', fill=True, clip=(1, 25))
    sns.kdeplot(df[df['Winner'] == 1]['GridPosition'], label='Winner', fill=True, color='gold', clip=(1, 25))
    plt.title('Starting Grid Position: Winners vs. Non-Winners (2014-Present)', fontsize=16)
    plt.xlabel('Grid Position')
    plt.legend()
    plt.gca().invert_xaxis() # Put P1 on the left
    plt.show()