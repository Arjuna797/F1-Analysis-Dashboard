import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# These are the original features BEFORE API data
MODEL_FEATURES = [
    'GridPosition',
    'PositionChange',
    'TeamPerformanceScore',
    'Temperature',
    'RainProbability'
]

# This is the target we want to predict
MODEL_TARGET = 'Winner'

def train_model(df):
    """
    Trains a RandomForest model to find feature importances.
    """
    print("Training model...")
    
    # 1. Select data from a modern era
    df_model = df[df['year'] >= 2014].copy()
    
    # 2. Define Features (X) and Target (y)
    X = df_model[MODEL_FEATURES]
    y = df_model[MODEL_TARGET]
    
    # 3. Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 5. Initialize and Train Model
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train_scaled, y_train)
    
    # 6. Evaluate Model
    y_pred = model.predict(X_test_scaled)
    print("\n--- Model Evaluation Report ---")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # 7. Get Feature Importances
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': MODEL_FEATURES,
        'importance': importances
    }).sort_values(by='importance', ascending=False)
    
    print("Model training complete.")
    
    # Return the full dataset (for plotting) and the importances
    return df_model, feature_importance_df