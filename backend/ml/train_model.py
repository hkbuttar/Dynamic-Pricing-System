import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import math

def create_synthetic_data():
    """Create synthetic training data for the pricing model"""
    np.random.seed(42)
    n_samples = 5000
    
    # Generate realistic product data
    prices = np.random.uniform(10, 500, n_samples)
    inventory = np.random.randint(1, 100, n_samples)
    ratings = np.random.uniform(1.0, 5.0, n_samples)
    
    # Create categories
    categories = ['Electronics', 'Apparel', 'Home', 'Books', 'Sports']
    category_idx = np.random.randint(0, len(categories), n_samples)
    
    # Category multipliers
    category_effects = {
        0: 1.3,  # Electronics
        1: 1.0,  # Apparel  
        2: 0.9,  # Home
        3: 0.7,  # Books
        4: 1.1   # Sports
    }
    
    # Generate sales with realistic relationships
    sales = []
    for i in range(n_samples):
        # Base demand influenced by price elasticity
        price_effect = max(0, 150 - 0.5 * prices[i])  # Price elasticity
        
        # Inventory effect (more inventory = higher visibility)
        inventory_effect = min(20, 0.3 * inventory[i])
        
        # Rating effect (better ratings = more sales)
        rating_effect = 30 * (ratings[i] - 1)  # Scale 1-5 to 0-120
        
        # Category effect
        category_effect = price_effect * category_effects[category_idx[i]]
        
        # Combine effects with some noise
        total_sales = (
            category_effect + 
            inventory_effect + 
            rating_effect + 
            np.random.normal(0, 15)  # Random noise
        )
        
        # Ensure non-negative sales
        sales.append(max(0, total_sales))
    
    return prices, inventory, ratings, category_idx, np.array(sales)

def train_model():
    """Train the pricing optimization model"""
    print("Creating synthetic training data...")
    prices, inventory, ratings, categories, sales = create_synthetic_data()
    
    # Prepare features
    X = np.column_stack([prices, inventory, ratings, categories])
    y = sales
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train multiple models and choose the best
    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_score = -float('inf')
    best_name = ""
    
    print("Training models...")
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        print(f"{name}: R² = {r2:.4f}, RMSE = {rmse:.2f}")
        
        if r2 > best_score:
            best_score = r2
            best_model = model
            best_name = name
    
    print(f"Best model: {best_name} with R² = {best_score:.4f}")
    
    # Save the best model
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    with open(model_path, "wb") as f:
        pickle.dump(best_model, f)
    
    print(f"Model saved to {model_path}")
    
    # Create feature importance report for Random Forest
    if best_name == 'RandomForest':
        feature_names = ['Price', 'Inventory', 'Rating', 'Category']
        importances = best_model.feature_importances_
        
        print("\nFeature Importance:")
        for name, importance in zip(feature_names, importances):
            print(f"{name}: {importance:.4f}")
    
    return best_model

if __name__ == "__main__":
    train_model()