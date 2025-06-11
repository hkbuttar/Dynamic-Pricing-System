import React, { useState } from "react";
import axios from "axios";

function App() {
  const [products, setProducts] = useState([]);

  const fetchPrices = async () => {
    const response = await axios.post("http://localhost:5000/api/prices", [
      {
        product_id: "P001",
        base_price: 100.0,
        inventory: 15,
        sales_last_30_days: 120,
        average_rating: 4.5,
        category: "Electronics"
      }
    ]);
    setProducts(response.data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Dynamic Pricing Dashboard</h1>
      <button onClick={fetchPrices}>Fetch Adjusted Prices</button>
      <ul>
        {products.map((p) => (
          <li key={p.product_id}>
            {p.product_id}: ${p.adjusted_price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;