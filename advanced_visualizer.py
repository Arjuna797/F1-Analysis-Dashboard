import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_winner_profiles_violin(df):
    """
    Shows a side-by-side comparison of Winners vs. Non-Winners across key metrics.
    A violin plot is like a box plot but also shows the probability density of the data.
    """
    print("Displaying Winner Profile Violin Plots...")
    
    # Filter for modern era and select key features
    plot_df = df[df['year'] >= 2014].copy()
    plot_df['Winner'] = plot_df['Winner'].map({1: 'Winner', 0: 'Non-Winner'})

    fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    fig.suptitle('How Do Winners Differ from the Rest of the Field?', fontsize=20)

    # Plot 1: Team Performance Score
    sns.violinplot(ax=axes[0], x='Winner', y='TeamPerformanceScore', data=plot_df, palette={'Winner':'gold', 'Non-Winner':'skyblue'}, cut=0)
    axes[0].set_title('Winners Drive for Better Performing Teams', fontsize=14)
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Team Performance Score (Season Avg Points)')

    # Plot 2: Grid Position
    sns.violinplot(ax=axes[1], x='Winner', y='GridPosition', data=plot_df, palette={'Winner':'gold', 'Non-Winner':'skyblue'})
    axes[1].set_title('Winners Start at the Front of the Grid', fontsize=14)
    axes[1].set_xlabel('Race Outcome', fontsize=12)
    axes[1].set_ylabel('Starting Grid Position')
    axes[1].invert_yaxis() # P1 at the top

    # Plot 3: Position Change
    sns.violinplot(ax=axes[2], x='Winner', y='PositionChange', data=plot_df, palette={'Winner':'gold', 'Non-Winner':'skyblue'})
    axes[2].set_title('Winners Generally Maintain Their Position', fontsize=14)
    axes[2].set_xlabel('')
    axes[2].set_ylabel('Positions Gained / Lost')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def plot_grid_vs_performance_2d_scatter(df):
    """
    A clear 2D scatter plot showing the two most important factors:
    Grid Position vs. Team Performance.
    """
    print("Displaying 2D Scatter Plot of Top Factors...")
    
    plot_df = df[df['year'] >= 2014].copy()
    
    plt.figure(figsize=(12, 8))
    
    sns.scatterplot(
        x='GridPosition',
        y='TeamPerformanceScore',
        data=plot_df,
        hue='Winner',
        palette={1: 'gold', 0: 'navy'},
        alpha=0.6,
        s=50 # marker size
    )
    
    plt.title('The Winning Zone: Grid Position vs. Team Performance', fontsize=16)
    plt.xlabel('Starting Grid Position')
    plt.ylabel('Team Performance Score')
    plt.gca().invert_xaxis() # P1 on the left
    plt.legend(title='Race Outcome', labels=['Winner', 'Non-Winner'])
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def plot_rain_impact_swarm(df):
    """
    A swarm plot shows how rain affects the finishing positions of drivers.
    In chaotic, wet races, results are more spread out.
    """
    print("Displaying Rain Impact Swarm Plot...")
    
    # Let's focus on races with a significant chance of rain vs. dry races
    rainy_races = df[df['RainProbability'] >= 0.5]
    dry_races = df[df['RainProbability'] == 0].sample(n=len(rainy_races), random_state=42) # Sample for a cleaner plot
    
    plot_df = pd.concat([rainy_races, dry_races])
    plot_df['Race Condition'] = plot_df['RainProbability'].apply(lambda x: 'Rainy (>=50% Prob)' if x > 0 else 'Dry')
    
    plt.figure(figsize=(12, 8))
    sns.swarmplot(
        x='Race Condition',
        y='finalPosition',
        data=plot_df,
        palette={'Dry': 'skyblue', 'Rainy (>=50% Prob)': 'darkslateblue'},
        order=['Dry', 'Rainy (>=50% Prob)'],
        s=4 # smaller points
    )
    
    plt.title('Race Results Are More Spread Out in the Rain', fontsize=16)
    plt.xlabel('Race Condition')
    plt.ylabel('Final Finishing Position')
    plt.ylim(0, 22)
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()