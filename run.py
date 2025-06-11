import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Starting Dynamic Pricing System Backend...")
print("Current directory:", current_dir)

try:
    from backend import create_app
    app = create_app()
    print("✅ Successfully imported and created app")
except Exception as e:
    print(f"❌ Import failed: {e}")
    print("Creating fallback app...")
    
    from flask import Flask, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route("/")
    def home():
        return jsonify({"message": "Dynamic Pricing API is running - Fallback mode"})
    
    @app.route("/api/health")
    def health():
        return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("API will be available at: http://localhost:5000")
    
    # Show registered routes
    print("\n📋 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} {list(rule.methods)}")
    
    print("\n🔍 Health check: http://localhost:5000/api/health")
    if any("api/products" in str(rule) for rule in app.url_map.iter_rules()):
        print("📊 Products endpoint: http://localhost:5000/api/products")
        print("💰 Pricing endpoint: http://localhost:5000/api/prices")
        print("🏪 Competitor endpoint: http://localhost:5000/api/competitor-prices")
    
    print("\n" + "="*50)
    
    app.run(debug=True, host="0.0.0.0", port=5000)