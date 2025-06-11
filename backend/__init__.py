from flask import Flask
from flask_cors import CORS
import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Import and register blueprint
    try:
        from .app.routes import api_blueprint
        app.register_blueprint(api_blueprint)
        print("✅ Blueprint registered successfully via relative import")
    except ImportError:
        try:
            from .app.routes import api_blueprint
            app.register_blueprint(api_blueprint)
            print("✅ Blueprint registered successfully via direct import")
        except ImportError as e:
            print(f"❌ Failed to import routes: {e}")
            
            # Create basic fallback routes
            @app.route("/")
            def home():
                return {"message": "API running - routes import failed"}
            
            @app.route("/api/health")
            def health():
                return {"status": "healthy"}
    
    return app