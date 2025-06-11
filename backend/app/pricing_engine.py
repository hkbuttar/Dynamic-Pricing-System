import pickle
import numpy as np

with open("ml/model.pkl", "rb") as f:
    model = pickle.load(f)

def get_adjusted_prices(data):
    results = []
    for product in data:
        base = product["base_price"]
        inventory = product["inventory"]
        sales = product["sales_last_30_days"]
        rating = product["average_rating"]

        # Predict demand based on base price
        predicted_sales = model.predict(np.array([[base]]))[0]

        adjusted_price = base

        # Business rules
        if inventory < 10:
            adjusted_price = min(base * 1.3, base * 1.5)
        elif predicted_sales < 20:
            adjusted_price = max(base * 0.8, base * 1.1)

        # Profit margin enforcement
        adjusted_price = max(adjusted_price, base * 1.1)
        adjusted_price = min(adjusted_price, base * 1.5)

        product["adjusted_price"] = round(adjusted_price, 2)
        results.append(product)
    return results