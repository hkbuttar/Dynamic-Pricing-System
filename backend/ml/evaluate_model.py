import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error

with open("ml/model.pkl", "rb") as f:
    model = pickle.load(f)

df = pd.read_csv("backend/data/historical_sales.csv")
X = df[["price"]]
y_true = df["units_sold"]
y_pred = model.predict(X)

rmse = mean_squared_error(y_true, y_pred, squared=False)
print("RMSE:", rmse)