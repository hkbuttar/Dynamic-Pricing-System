import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer
} from "recharts";
import styled from "styled-components";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5000";

const Dashboard = styled.div`
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
`;

const Header = styled.h1`
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2.5rem;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const StatCard = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 5px;
`;

const StatLabel = styled.div`
  font-size: 0.9rem;
  color: #7f8c8d;
`;

const ChartGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const ChartCard = styled.div`
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
`;

const ChartTitle = styled.h3`
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
`;

const ProductTable = styled.table`
  width: 100%;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-collapse: collapse;
  overflow: hidden;
`;

const TableHeader = styled.th`
  background: #3498db;
  color: white;
  padding: 15px;
  text-align: left;
`;

const TableCell = styled.td`
  padding: 12px 15px;
  border-bottom: 1px solid #ecf0f1;
`;

const TableRow = styled.tr`
  &:hover {
    background-color: #f8f9fa;
  }
`;

const PriceChange = styled.span`
  font-weight: bold;
  color: ${props => props.positive ? '#27ae60' : '#e74c3c'};
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 1.2rem;
  color: #7f8c8d;
`;

const RefreshButton = styled.button`
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 10px;
  
  &:hover {
    background: #2980b9;
  }
  
  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
`;

const COLORS = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6'];

function App() {
  const [products, setProducts] = useState([]);
  const [competitorData, setCompetitorData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({});
  const [connectionStatus, setConnectionStatus] = useState("unknown");

  const testConnection = async () => {
    console.log("🧪 Testing connection to backend...");
    console.log("API_BASE URL:", API_BASE);
    
    try {
      const response = await axios.get(`${API_BASE}/api/health`, {
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log("✅ Connection test successful:", response.data);
      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);
      
      setConnectionStatus("connected");
      alert(`✅ Backend connection successful!\n\nStatus: ${response.data.status}\nAPI URL: ${API_BASE}`);
    } catch (error) {
      console.error("❌ Connection test failed:", error);
      console.error("Error details:", {
        message: error.message,
        code: error.code,
        status: error.response?.status,
        statusText: error.response?.statusText,
        url: error.config?.url
      });
      
      setConnectionStatus("failed");
      
      let errorMessage = `Connection failed to ${API_BASE}`;
      
      if (error.code === 'ECONNREFUSED') {
        errorMessage += "\n\n❌ Connection refused - Backend server is not running";
      } else if (error.code === 'ETIMEDOUT') {
        errorMessage += "\n\n⏰ Connection timed out - Backend server may be slow or unresponsive";
      } else if (error.message.includes('Network Error')) {
        errorMessage += "\n\n🌐 Network error - Check if backend server is accessible";
      } else if (error.response?.status === 404) {
        errorMessage += "\n\n❌ 404 Not Found - API endpoint doesn't exist";
      } else {
        errorMessage += `\n\n${error.message}`;
      }
      
      errorMessage += "\n\nTroubleshooting:\n1. Make sure backend is running: python run.py\n2. Check backend is on port 5000\n3. Verify no firewall blocking connection";
      
      alert(errorMessage);
    }
  };

  const fetchData = async () => {
    setLoading(true);
    console.log("🔄 Starting data fetch...");
    console.log("API_BASE:", API_BASE);
    
    try {
      // Test backend connection first
      console.log("Testing backend connection...");
      const healthCheck = await axios.get(`${API_BASE}/api/health`, {
        timeout: 10000,
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log("✅ Health check successful:", healthCheck.data);
      
      console.log("Fetching products and competitor data...");
      const [productsRes, competitorRes] = await Promise.all([
        axios.get(`${API_BASE}/api/products`, {
          timeout: 10000,
          headers: {
            'Content-Type': 'application/json',
          }
        }),
        axios.get(`${API_BASE}/api/competitor-prices`, {
          timeout: 10000,
          headers: {
            'Content-Type': 'application/json',
          }
        })
      ]);
      
      console.log("✅ Products data received:", productsRes.data.length, "products");
      console.log("✅ Competitor data received:", competitorRes.data.length, "competitors");
      
      setProducts(productsRes.data);
      setCompetitorData(competitorRes.data);
      calculateStats(productsRes.data);
      setConnectionStatus("connected");
      
      console.log("✅ Data fetch completed successfully!");
    } catch (error) {
      console.error("❌ Detailed error:", error);
      console.error("Error message:", error.message);
      console.error("Error code:", error.code);
      console.error("Error response:", error.response?.data);
      console.error("Error status:", error.response?.status);
      console.error("Error config URL:", error.config?.url);
      
      setConnectionStatus("failed");
      
      let errorMessage = "Unknown error occurred";
      
      if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
        errorMessage = "Cannot connect to backend server. Make sure backend is running on port 5000.";
      } else if (error.response?.status === 404) {
        errorMessage = `API endpoint not found: ${error.config?.url}`;
      } else if (error.response?.status >= 500) {
        errorMessage = `Server error: ${error.response?.data?.error || error.message}`;
      } else if (error.response?.data?.error) {
        errorMessage = error.response.data.error;
      } else {
        errorMessage = error.message;
      }
      
      alert(`❌ Error fetching data: ${errorMessage}\n\nCheck browser console (F12) for detailed logs.`);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (productData) => {
    const totalProducts = productData.length;
    const avgPriceIncrease = productData.reduce((sum, p) => sum + p.price_change_percent, 0) / totalProducts;
    const totalRevenueImpact = productData.reduce((sum, p) => sum + (p.revenue_impact || 0), 0);
    const highInventoryCount = productData.filter(p => p.inventory > 50).length;
    
    setStats({
      totalProducts,
      avgPriceIncrease: avgPriceIncrease.toFixed(2),
      totalRevenueImpact: totalRevenueImpact.toFixed(0),
      highInventoryCount
    });
  };

  useEffect(() => {
    console.log("🚀 Component mounted, fetching initial data...");
    fetchData();
  }, []);

  const prepareChartData = () => {
    return products.map(p => ({
      name: p.product_id,
      basePrice: p.base_price,
      adjustedPrice: p.adjusted_price,
      priceChange: p.price_change_percent,
      inventory: p.inventory,
      sales: p.sales_last_30_days,
      rating: p.average_rating
    }));
  };

  const prepareCategoryData = () => {
    const categoryStats = {};
    products.forEach(p => {
      if (!categoryStats[p.category]) {
        categoryStats[p.category] = { count: 0, totalRevenue: 0 };
      }
      categoryStats[p.category].count++;
      categoryStats[p.category].totalRevenue += p.revenue_impact || 0;
    });
    
    return Object.entries(categoryStats).map(([category, data]) => ({
      name: category,
      count: data.count,
      revenue: data.totalRevenue.toFixed(0)
    }));
  };

  const prepareCompetitorComparisonData = () => {
    return products.map(p => {
      const competitor = competitorData.find(c => c.product_id === p.product_id);
      return {
        name: p.product_id,
        ourPrice: p.adjusted_price,
        competitorPrice: competitor?.competitor_price || 0,
        advantage: competitor ? ((competitor.competitor_price - p.adjusted_price) / p.adjusted_price * 100).toFixed(1) : 0
      };
    });
  };

  return (
    <Dashboard>
      <Header>Dynamic Pricing Dashboard</Header>
      
      <div style={{ marginBottom: "20px", display: "flex", gap: "10px", alignItems: "center" }}>
        <RefreshButton onClick={fetchData} disabled={loading}>
          {loading ? "Loading..." : "Refresh Data"}
        </RefreshButton>
        
        <RefreshButton onClick={testConnection} style={{ background: "#27ae60" }}>
          Test Connection
        </RefreshButton>
        
        <div style={{ 
          padding: "8px 16px", 
          borderRadius: "4px", 
          fontSize: "14px",
          background: connectionStatus === "connected" ? "#d4edda" : 
                     connectionStatus === "failed" ? "#f8d7da" : "#e2e3e5",
          color: connectionStatus === "connected" ? "#155724" : 
                 connectionStatus === "failed" ? "#721c24" : "#383d41",
          border: `1px solid ${connectionStatus === "connected" ? "#c3e6cb" : 
                                connectionStatus === "failed" ? "#f5c6cb" : "#ced4da"}`
        }}>
          Backend: {connectionStatus === "connected" ? "✅ Connected" : 
                   connectionStatus === "failed" ? "❌ Disconnected" : "❓ Unknown"}
        </div>
      </div>

      {loading ? (
        <LoadingSpinner>Loading pricing data...</LoadingSpinner>
      ) : (
        <>
          <StatsGrid>
            <StatCard>
              <StatValue>{stats.totalProducts || 0}</StatValue>
              <StatLabel>Total Products</StatLabel>
            </StatCard>
            <StatCard>
              <StatValue>{stats.avgPriceIncrease || 0}%</StatValue>
              <StatLabel>Avg Price Change</StatLabel>
            </StatCard>
            <StatCard>
              <StatValue>${stats.totalRevenueImpact || 0}</StatValue>
              <StatLabel>Revenue Impact</StatLabel>
            </StatCard>
            <StatCard>
              <StatValue>{stats.highInventoryCount || 0}</StatValue>
              <StatLabel>High Inventory Items</StatLabel>
            </StatCard>
          </StatsGrid>

          {products.length > 0 ? (
            <>
              <ChartGrid>
                <ChartCard>
                  <ChartTitle>Price Adjustments by Product</ChartTitle>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={prepareChartData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="basePrice" fill="#95a5a6" name="Base Price" />
                      <Bar dataKey="adjustedPrice" fill="#3498db" name="Adjusted Price" />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartCard>

                <ChartCard>
                  <ChartTitle>Category Distribution</ChartTitle>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={prepareCategoryData()}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, count }) => `${name} (${count})`}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="count"
                      >
                        {prepareCategoryData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </ChartCard>
              </ChartGrid>

              <ChartCard>
                <ChartTitle>Product Details</ChartTitle>
                <ProductTable>
                  <thead>
                    <tr>
                      <TableHeader>Product ID</TableHeader>
                      <TableHeader>Category</TableHeader>
                      <TableHeader>Base Price</TableHeader>
                      <TableHeader>Adjusted Price</TableHeader>
                      <TableHeader>Change %</TableHeader>
                      <TableHeader>Inventory</TableHeader>
                      <TableHeader>Sales (30d)</TableHeader>
                      <TableHeader>Rating</TableHeader>
                      <TableHeader>Revenue Impact</TableHeader>
                      <TableHeader>Rule Applied</TableHeader>
                    </tr>
                  </thead>
                  <tbody>
                    {products.map((product) => (
                      <TableRow key={product.product_id}>
                        <TableCell>{product.product_id}</TableCell>
                        <TableCell>{product.category}</TableCell>
                        <TableCell>${product.base_price}</TableCell>
                        <TableCell>${product.adjusted_price}</TableCell>
                        <TableCell>
                          <PriceChange positive={product.price_change_percent > 0}>
                            {product.price_change_percent > 0 ? '+' : ''}{product.price_change_percent}%
                          </PriceChange>
                        </TableCell>
                        <TableCell>{product.inventory}</TableCell>
                        <TableCell>{product.sales_last_30_days}</TableCell>
                        <TableCell>{product.average_rating}</TableCell>
                        <TableCell>
                          <PriceChange positive={product.revenue_impact > 0}>
                            ${product.revenue_impact}
                          </PriceChange>
                        </TableCell>
                        <TableCell>{product.rule_applied}</TableCell>
                      </TableRow>
                    ))}
                  </tbody>
                </ProductTable>
              </ChartCard>
            </>
          ) : (
            <div style={{ textAlign: "center", padding: "40px" }}>
              <h3>No data available</h3>
              <p>Click "Test Connection" to check backend connectivity</p>
            </div>
          )}
        </>
      )}
    </Dashboard>
  );
}

export default App;
