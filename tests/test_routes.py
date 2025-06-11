from app import create_app
import json

def test_api():
    app = create_app()
    client = app.test_client()
    response = client.post("/api/prices", json=[{
        "product_id": "P001",
        "base_price": 100.0,
        "inventory": 15,
        "sales_last_30_days": 120,
        "average_rating": 4.5,
        "category": "Electronics"
    }])
    assert response.status_code == 200
    data = response.get_json()
    assert "adjusted_price" in data[0]