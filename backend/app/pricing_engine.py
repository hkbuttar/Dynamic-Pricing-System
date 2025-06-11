import pickle
import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LinearRegression

def ensure_model_exists():
    """Ensure ML model exists, create if not"""
    model_path = os.path.join(os.path.dirname(__file__), "ml", "model.pkl")
    
    if not os.path.exists(model_path):
        print("Model not found, creating simple model...")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Create simple training data
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic training data
        prices = np.random.uniform(10, 500, n_samples)
        inventory = np.random.randint(1, 100, n_samples)
        ratings = np.random.uniform(1, 5, n_samples)
        
        # Create realistic sales based on price, inventory, and rating
        sales = (
            100 - 0.3 * prices +  # Price elasticity
            0.2 * inventory +     # Inventory effect
            20 * ratings +        # Rating effect
            np.random.normal(0, 10, n_samples)  # Noise
        )
        sales = np.maximum(sales, 0)  # Ensure non-negative sales
        
        # Create and train model
        X = np.column_stack([prices, inventory, ratings])
        model = LinearRegression()
        model.fit(X, sales)
        
        # Save model
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        print(f"Model saved to {model_path}")
    
    return model_path

def load_model():
    """Load the ML model with fallback"""
    try:
        model_path = ensure_model_exists()
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"Warning: Could not load ML model: {e}")
        print("Using fallback simple model...")
        
        # Create a simple fallback model
        class FallbackModel:
            def predict(self, X):
                # Simple prediction: sales inversely related to price
                if len(X.shape) == 1:
                    X = X.reshape(1, -1)
                
                results = []
                for row in X:
                    price = row[0]
                    inventory = row[1] if len(row) > 1 else 50
                    rating = row[2] if len(row) > 2 else 4.0
                    
                    # Simple formula
                    predicted_sales = max(0, 100 - 0.2 * price + 0.1 * inventory + 10 * rating)
                    results.append(predicted_sales)
                
                return np.array(results)
        
        return FallbackModel()

def get_competitor_price(product_id):
    """Mock function to get competitor price"""
    # Mock competitor prices
    competitor_prices = {
        "P001": 90.0,
        "P002": 195.0,
        "P003": 48.0,
        "P004": 72.0,
        "P005": 145.0
    }
    return competitor_prices.get(product_id, None)

def calculate_demand_multiplier(sales_last_30_days, category):
    """Calculate demand multiplier based on sales and category"""
    category_multipliers = {
        "Electronics": 1.2,
        "Apparel": 1.0,
        "Home": 0.9
    }
    
    base_multiplier = category_multipliers.get(category, 1.0)
    
    # Adjust based on sales performance
    if sales_last_30_days > 100:
        return base_multiplier * 1.1  # High demand
    elif sales_last_30_days < 20:
        return base_multiplier * 0.9  # Low demand
    else:
        return base_multiplier

def get_adjusted_prices(data):
    """
    Advanced pricing engine with ML integration and business rules
    """
    try:
        model = load_model()
        print("✅ ML model loaded successfully")
    except Exception as e:
        print(f"❌ ML model load failed: {e}")
        
        # Simple fallback pricing without ML
        def simple_pricing(products):
            results = []
            for product in products:
                base_price = product["base_price"]
                inventory = product["inventory"]
                sales = product["sales_last_30_days"]
                
                # Simple rules
                if inventory < 10:
                    adjusted_price = base_price * 1.2
                    rule_applied = "Low inventory: +20%"
                elif sales > 100:
                    adjusted_price = base_price * 1.1
                    rule_applied = "High demand: +10%"
                else:
                    adjusted_price = base_price * 1.05
                    rule_applied = "Standard: +5%"
                
                # Constraints
                adjusted_price = max(base_price * 1.1, min(adjusted_price, base_price * 1.5))
                
                product_result = product.copy()
                product_result.update({
                    "adjusted_price": round(adjusted_price, 2),
                    "price_change_percent": round(((adjusted_price - base_price) / base_price) * 100, 2),
                    "predicted_sales": round(sales * 0.95, 1),
                    "competitor_price": get_competitor_price(product["product_id"]),
                    "revenue_impact": round((adjusted_price - base_price) * sales, 2),
                    "rule_applied": rule_applied,
                    "demand_multiplier": 1.0
                })
                results.append(product_result)
            
            return results
        
        return simple_pricing(data)
    
    # Full ML-based pricing logic
    results = []
    
    for product in data:
        base_price = product["base_price"]
        inventory = product["inventory"]
        sales = product["sales_last_30_days"]
        rating = product["average_rating"]
        category = product.get("category", "General")
        product_id = product["product_id"]
        
        # ML prediction for optimal sales
        features = np.array([[base_price, inventory, rating]])
        predicted_sales = model.predict(features)[0]
        
        # Calculate base adjustment from ML model
        current_sales = sales
        if predicted_sales > current_sales * 1.2:
            # Model suggests higher sales possible, can increase price slightly
            ml_adjustment = 1.05
        elif predicted_sales < current_sales * 0.8:
            # Model suggests lower sales likely, decrease price
            ml_adjustment = 0.95
        else:
            ml_adjustment = 1.0
        
        # Start with ML-adjusted price
        adjusted_price = base_price * ml_adjustment
        
        # Apply demand multiplier based on category and sales
        demand_multiplier = calculate_demand_multiplier(sales, category)
        adjusted_price *= demand_multiplier
        
        # Business Rule 1: Inventory-based pricing
        if inventory < 10:
            # Low inventory - increase price (scarcity pricing)
            inventory_multiplier = min(1.3, 1.0 + (10 - inventory) * 0.03)
            adjusted_price *= inventory_multiplier
            rule_applied = f"Low inventory rule: +{(inventory_multiplier-1)*100:.1f}%"
        elif inventory > 80:
            # High inventory - decrease price to move stock
            inventory_multiplier = max(0.9, 1.0 - (inventory - 80) * 0.005)
            adjusted_price *= inventory_multiplier
            rule_applied = f"High inventory rule: {(inventory_multiplier-1)*100:.1f}%"
        else:
            rule_applied = "Normal inventory"
        
        # Business Rule 2: Competitor pricing
        competitor_price = get_competitor_price(product_id)
        if competitor_price:
            competitor_ratio = competitor_price / base_price
            if competitor_ratio < 0.8:  # Competitor significantly undercuts
                # Reduce price but maintain minimum margin
                competitive_price = max(competitor_price * 1.05, base_price * 1.1)
                if competitive_price < adjusted_price:
                    adjusted_price = competitive_price
                    rule_applied += f"; Competitive response to ${competitor_price}"
        
        # Business Rule 3: Rating-based adjustments
        if rating >= 4.5:
            # Premium pricing for highly rated products
            adjusted_price *= 1.02
        elif rating < 3.5:
            # Discount for poorly rated products
            adjusted_price *= 0.98
        
        # Business Rule 4: Profit margin constraints
        min_price = base_price * 1.1  # Cost + 10% minimum margin
        max_price = base_price * 1.5  # Maximum 50% markup
        
        adjusted_price = max(min_price, min(adjusted_price, max_price))
        
        # Calculate metrics
        price_change_percent = ((adjusted_price - base_price) / base_price) * 100
        revenue_impact = (adjusted_price - base_price) * sales
        
        # Add results
        product_result = product.copy()
        product_result.update({
            "adjusted_price": round(adjusted_price, 2),
            "price_change_percent": round(price_change_percent, 2),
            "predicted_sales": round(predicted_sales, 1),
            "competitor_price": competitor_price,
            "revenue_impact": round(revenue_impact, 2),
            "rule_applied": rule_applied,
            "demand_multiplier": round(demand_multiplier, 3)
        })
        
        results.append(product_result)
    
    return results