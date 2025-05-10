import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
df = pd.read_csv("./datasets/cleaned_crime_data.csv")
df = df.dropna()

# Prepare features and target
def prepare_data(df):
    # Select features for prediction
    features = [
        'Year', 'Month', 'Latitude', 'Longitude',
        'Primary Type', 'Description', 'generalized_loc'
    ]
    
    # Create target variable (crime count per location per month)
    df['crime_count'] = df.groupby(['Year', 'Month', 'Latitude', 'Longitude'])['Primary Type'].transform('count')
    
    # Prepare features
    X = df[features].copy()
    y = df['crime_count']
    
    # Encode categorical variables
    le = LabelEncoder()
    X['Primary Type'] = le.fit_transform(X['Primary Type'])
    X['Description'] = le.fit_transform(X['Description'])
    X['generalized_loc'] = le.fit_transform(X['generalized_loc'])
    
    return X, y

# Function to evaluate models
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation score
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    
    print(f"\n{model_name} Results:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R2 Score: {r2:.2f}")
    print(f"Cross-validation scores: {cv_scores.mean():.2f} (+/- {cv_scores.std() * 2:.2f})")
    
    return model, y_pred

# Function to plot feature importance for tree-based models
def plot_feature_importance(model, X, model_name):
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        features = X.columns
        
        # Create DataFrame for plotting
        feature_importance = pd.DataFrame({
            'Feature': features,
            'Importance': importance
        }).sort_values('Importance', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importance)
        plt.title(f'Feature Importance - {model_name}')
        plt.tight_layout()
        plt.show()

def main():
    # Prepare data
    X, y = prepare_data(df)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize models
    models = {
        'KNN': KNeighborsRegressor(n_neighbors=5),
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42)
    }
    
    # Train and evaluate each model
    results = {}
    for name, model in models.items():
        trained_model, predictions = evaluate_model(
            model, X_train_scaled, X_test_scaled, y_train, y_test, name
        )
        results[name] = {
            'model': trained_model,
            'predictions': predictions
        }
        
        # Plot feature importance for tree-based models
        if name in ['Random Forest', 'XGBoost']:
            plot_feature_importance(trained_model, X, name)
    
    # Compare models
    plt.figure(figsize=(10, 6))
    for name, result in results.items():
        plt.scatter(y_test, result['predictions'], alpha=0.5, label=name)
    
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Model Comparison: Actual vs Predicted Values')
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main() 