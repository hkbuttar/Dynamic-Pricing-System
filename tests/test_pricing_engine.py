from app.pricing_engine import get_adjusted_prices

def test_adjusted_price():
    sample = [{
        "product_id": "P001",
        "base_price": 100.0,
        "inventory": 5,
        "sales_last_30_days": 120,
        "average_rating": 4.5,
        "category": "Electronics"
    }]
    results = get_adjusted_prices(sample)
    assert results[0]["adjusted_price"] >= 110.0
    assert results[0]["adjusted_price"] <= 150.0