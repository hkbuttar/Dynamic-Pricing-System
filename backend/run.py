import os
import sys
from flask import Flask
from flask_cors import CORS

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Try to import and register the blueprint
    try:
        from backend import create_app as backend_create_app
        return backend_create_app()
    except ImportError as e:
        print(f"Import error with backend.__init__: {e}")
        print("Trying direct blueprint import...")
        
        try:
            from backend.routes import api_blueprint
            app.register_blueprint(api_blueprint)
            print("✅ Successfully registered API blueprint")
            return app
        except ImportError as e2:
            print(f"Direct import error: {e2}")
            print("Creating fallback app...")
            
            # Fallback: create basic routes directly
            @app.route("/")
            def home():
                return {"message": "Dynamic Pricing API is running - Fallback mode"}
            
            @app.route("/api/health")  
            def health():
                return {"status": "healthy"}
                
            return app

if __name__ == "__main__":
    print("Starting Dynamic Pricing System Backend...")
    print("API will be available at: http://localhost:5000")
    
    app = create_app()
    
    # Debug: Show registered routes
    print("\n📋 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} {list(rule.methods)}")
    
    print("\n🔍 Health check: http://localhost:5000/api/health")
    print("📊 Products endpoint: http://localhost:5000/api/products")
    print("💰 Pricing endpoint: http://localhost:5000/api/prices")
    print("🏪 Competitor endpoint: http://localhost:5000/api/competitor-prices")
    print("🐛 Debug routes: http://localhost:5000/api/debug/routes")
    print("\n" + "="*50)
    
    app.run(debug=True, host="0.0.0.0", port=5000)