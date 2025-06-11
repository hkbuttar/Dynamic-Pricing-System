import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load comprehensive historical sales data
df = pd.read_csv("data/historical_sales.csv")
X = df[["price"]]
y = df["units_sold"]

model = LinearRegression().fit(X, y)

with open("ml/model.pkl", "wb") as f:
    pickle.dump(model, f)