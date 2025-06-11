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

const API_BASE = "http://localhost:5000";

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
  margin-bottom: 20px;
  
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

  const fetchData = async () => {
    setLoading(true);
    try {
      const [productsRes, competitorRes] = await Promise.all([
        axios.get(`${API_BASE}/api/products`),
        axios.get(`${API_BASE}/api/competitor-prices`)
      ]);
      
      setProducts(productsRes.data);
      setCompetitorData(competitorRes.data);
      calculateStats(productsRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Error fetching data. Make sure the backend is running on port 5000.");
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
      
      <RefreshButton onClick={fetchData} disabled={loading}>
        {loading ? "Loading..." : "Refresh Data"}
      </RefreshButton>

      {loading ? (
        <LoadingSpinner>Loading pricing data...</LoadingSpinner>
      ) : (
        <>
          <StatsGrid>
            <StatCard>
              <StatValue>{stats.totalProducts}</StatValue>
              <StatLabel>Total Products</StatLabel>
            </StatCard>
            <StatCard>
              <StatValue>{stats.avgPriceIncrease}%</StatValue>
              <StatLabel>Avg Price Change</StatLabel>
            </StatCard>
            <StatCard>
              <StatValue>${stats.totalRevenueImpact}</StatValue>
              <StatLabel>Revenue Impact</StatLabel>
            </StatCard>
            <StatCard>
              <StatValue>{stats.highInventoryCount}</StatValue>
              <StatLabel>High Inventory Items</StatLabel>
            </StatCard>
          </StatsGrid>

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
              <ChartTitle>Sales vs Inventory Levels</ChartTitle>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={prepareChartData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Bar yAxisId="left" dataKey="sales" fill="#e74c3c" name="Sales (30 days)" />
                  <Line yAxisId="right" type="monotone" dataKey="inventory" stroke="#f39c12" name="Inventory" />
                </LineChart>
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

            <ChartCard>
              <ChartTitle>Competitor Price Comparison</ChartTitle>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={prepareCompetitorComparisonData()}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="ourPrice" fill="#3498db" name="Our Price" />
                  <Bar dataKey="competitorPrice" fill="#e74c3c" name="Competitor Price" />
                </BarChart>
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
      )}
    </Dashboard>
  );
}

export default App;