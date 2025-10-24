import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

# --- Functions from original visualizer.py ---

def plot_feature_importance(importance_df):
    """
    Creates a bar chart and returns the figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(ax=ax, x='importance', y='feature', data=importance_df, hue='feature', palette='viridis', legend=False)
    ax.set_title('Which Factor Decides the Race Winner?', fontsize=16)
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_ylabel('Feature', fontsize=12)
    plt.tight_layout()
    return fig

def plot_3d_scatter(df):
    """
    Creates the 3D scatter plot and returns the figure object.
    """
    winners = df[df['Winner'] == 1]
    non_winners = df[df['Winner'] == 0].sample(frac=0.1, random_state=42)
    plot_df = pd.concat([winners, non_winners])
    
    colors = plot_df['Winner'].map({1: 'gold', 0: 'blue'})
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(
        plot_df['GridPosition'], 
        plot_df['TeamPerformanceScore'], 
        plot_df['PositionChange'], 
        c=colors, 
        s=20,
        alpha=0.6
    )
    
    ax.set_title('3D Analysis of Race Winners', fontsize=16)
    ax.set_xlabel('Grid Position (Lower is better)')
    ax.set_ylabel('Team Performance Score')
    ax.set_zlabel('Positions Gained/Lost')
    
    gold_patch = plt.Line2D([0], [0], marker='o', color='w', label='Winner', markersize=10, markerfacecolor='gold')
    blue_patch = plt.Line2D([0], [0], marker='o', color='w', label='Non-Winner', markersize=10, markerfacecolor='blue')
    ax.legend(handles=[gold_patch, blue_patch])
    
    ax.invert_xaxis()
    return fig

def plot_grid_distribution(df):
    """
    Shows the distribution of starting positions and returns the figure object.
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.kdeplot(ax=ax, data=df[df['Winner'] == 0], x='GridPosition', label='Non-Winner', fill=True, clip=(1, 25))
    sns.kdeplot(ax=ax, data=df[df['Winner'] == 1], x='GridPosition', label='Winner', fill=True, color='gold', clip=(1, 25))
    ax.set_title('Starting Grid Position: Winners vs. Non-Winners (2014-Present)', fontsize=16)
    ax.set_xlabel('Grid Position')
    ax.legend()
    ax.invert_xaxis() 
    return fig

# --- Functions from advanced_visualizer.py ---

def plot_winner_profiles_violin(df):
    """
    Shows side-by-side violin plots and returns the figure object.
    """
    plot_df = df[df['year'] >= 2014].copy()
    plot_df['Winner'] = plot_df['Winner'].map({1: 'Winner', 0: 'Non-Winner'})

    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.suptitle('How Do Winners Differ from the Rest of the Field?', fontsize=20)

    sns.violinplot(ax=axes[0], x='Winner', y='TeamPerformanceScore', data=plot_df, palette={'Winner':'gold', 'Non-Winner':'skyblue'}, cut=0)
    axes[0].set_title('Winners Drive for Better Performing Teams', fontsize=14)
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Team Performance Score (Season Avg Points)')

    sns.violinplot(ax=axes[1], x='Winner', y='GridPosition', data=plot_df, palette={'Winner':'gold', 'Non-Winner':'skyblue'})
    axes[1].set_title('Winners Start at the Front of the Grid', fontsize=14)
    axes[1].set_xlabel('Race Outcome', fontsize=12)
    axes[1].set_ylabel('Starting Grid Position')
    axes[1].invert_yaxis() 

    sns.violinplot(ax=axes[2], x='Winner', y='PositionChange', data=plot_df, palette={'Winner':'gold', 'Non-Winner':'skyblue'})
    axes[2].set_title('Winners Generally Maintain Their Position', fontsize=14)
    axes[2].set_xlabel('')
    axes[2].set_ylabel('Positions Gained / Lost')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig

def plot_grid_vs_performance_2d_scatter(df):
    """
    A clear 2D scatter plot and returns the figure object.
    """
    plot_df = df[df['year'] >= 2014].copy()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.scatterplot(
        ax=ax,
        x='GridPosition',
        y='TeamPerformanceScore',
        data=plot_df,
        hue='Winner',
        palette={1: 'gold', 0: 'navy'},
        alpha=0.6,
        s=50
    )
    
    ax.set_title('The Winning Zone: Grid Position vs. Team Performance', fontsize=16)
    ax.set_xlabel('Starting Grid Position')
    ax.set_ylabel('Team Performance Score')
    ax.invert_xaxis() 
    ax.legend(title='Race Outcome', labels=['Winner', 'Non-Winner'])
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig

def plot_rain_impact_swarm(df):
    """
    A swarm plot and returns the figure object.
    """
    rainy_races = df[df['RainProbability'] >= 0.5]
    if rainy_races.empty:
        # Return an empty figure if no data
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No rainy race data to display.", ha='center', va='center')
        return fig
        
    dry_races = df[df['RainProbability'] == 0].sample(n=len(rainy_races), random_state=42)
    
    plot_df = pd.concat([rainy_races, dry_races])
    plot_df['Race Condition'] = plot_df['RainProbability'].apply(lambda x: 'Rainy (>=50% Prob)' if x > 0 else 'Dry')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.swarmplot(
        ax=ax,
        x='Race Condition',
        y='finalPosition',
        data=plot_df,
        palette={'Dry': 'skyblue', 'Rainy (>=50% Prob)': 'darkslateblue'},
        order=['Dry', 'Rainy (>=50% Prob)'],
        s=4 
    )
    
    ax.set_title('Race Results Are More Spread Out in the Rain', fontsize=16)
    ax.set_xlabel('Race Condition')
    ax.set_ylabel('Final Finishing Position')
    ax.set_ylim(0, 22)
    ax.invert_yaxis()
    ax.grid(True, linestyle='--', alpha=0.5)
    return fig
