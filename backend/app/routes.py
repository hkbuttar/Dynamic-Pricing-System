from flask import Blueprint, jsonify, request
import requests
import json
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.pricing_engine import get_adjusted_prices
except ImportError:
    try:
        from pricing_engine import get_adjusted_prices
    except ImportError:
        print("Warning: Could not import pricing_engine, using fallback")
        
        def get_adjusted_prices(products):
            """Fallback pricing logic"""
            results = []
            for product in products:
                base_price = product["base_price"]
                inventory = product["inventory"]
                sales = product["sales_last_30_days"]
                
                # Simple pricing rules
                if inventory < 10:
                    adjusted_price = base_price * 1.2
                    rule_applied = "Low inventory: +20%"
                else:
                    adjusted_price = base_price * 1.05
                    rule_applied = "Normal pricing: +5%"
                
                # Ensure constraints
                adjusted_price = max(base_price * 1.1, min(adjusted_price, base_price * 1.5))
                
                product_result = product.copy()
                product_result.update({
                    "adjusted_price": round(adjusted_price, 2),
                    "price_change_percent": round(((adjusted_price - base_price) / base_price) * 100, 2),
                    "revenue_impact": round((adjusted_price - base_price) * sales, 2),
                    "rule_applied": rule_applied,
                    "predicted_sales": round(sales * 0.95, 1),
                    "competitor_price": None,
                    "demand_multiplier": 1.0
                })
                results.append(product_result)
            
            return results

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Dynamic Pricing API is running", 
        "status": "healthy",
        "routes_registered": True
    })

@api_blueprint.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

@api_blueprint.route("/api/products", methods=["GET"])
def get_products():
    """Get all products with current pricing"""
    try:
        print("📊 Processing products request...")
        
        # Load sample product data
        products = [
            {"product_id": "P001", "base_price": 100.0, "inventory": 15, "sales_last_30_days": 120, "average_rating": 4.5, "category": "Electronics"},
            {"product_id": "P002", "base_price": 200.0, "inventory": 50, "sales_last_30_days": 40, "average_rating": 4.0, "category": "Apparel"},
            {"product_id": "P003", "base_price": 50.0, "inventory": 5, "sales_last_30_days": 10, "average_rating": 3.8, "category": "Home"},
            {"product_id": "P004", "base_price": 75.0, "inventory": 25, "sales_last_30_days": 80, "average_rating": 4.2, "category": "Electronics"},
            {"product_id": "P005", "base_price": 150.0, "inventory": 8, "sales_last_30_days": 60, "average_rating": 4.7, "category": "Apparel"}
        ]
        
        result = get_adjusted_prices(products)
        print(f"✅ Successfully processed {len(result)} products")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in get_products: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_blueprint.route("/api/prices", methods=["POST"])
def adjust_prices():
    """Adjust prices for provided products"""
    try:
        print("💰 Processing price adjustment request...")
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        result = get_adjusted_prices(data)
        print(f"✅ Successfully adjusted prices for {len(result)} products")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error in adjust_prices: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_blueprint.route("/api/competitor-prices", methods=["GET"])
def get_competitor_prices():
    """Get competitor prices (mock data)"""
    try:
        print("🏪 Processing competitor prices request...")
        
        # Mock competitor data since the API in assignment doesn't exist
        competitor_data = [
            {"product_id": "P001", "competitor_price": 90.0, "competitor_name": "CompetitorA"},
            {"product_id": "P002", "competitor_price": 195.0, "competitor_name": "CompetitorB"},
            {"product_id": "P003", "competitor_price": 48.0, "competitor_name": "CompetitorC"},
            {"product_id": "P004", "competitor_price": 72.0, "competitor_name": "CompetitorA"},
            {"product_id": "P005", "competitor_price": 145.0, "competitor_name": "CompetitorB"}
        ]
        
        print(f"✅ Successfully returned {len(competitor_data)} competitor prices")
        return jsonify(competitor_data)
    except Exception as e:
        print(f"❌ Error in get_competitor_prices: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Debug route to check registered routes
@api_blueprint.route("/api/debug/routes", methods=["GET"])
def debug_routes():
    """Debug endpoint to show all registered routes"""
    try:
        from flask import current_app
        routes = []
        for rule in current_app.url_map.iter_rules():
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "rule": str(rule)
            })
        return jsonify({"registered_routes": routes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500