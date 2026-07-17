-- Sales Data Analysis SQL Queries

-- View all records
SELECT * FROM sales_data;

-- Total Sales
SELECT SUM(Sales) AS Total_Sales
FROM sales_data;

-- Total Profit
SELECT SUM(Profit) AS Total_Profit
FROM sales_data;

-- Total Orders
SELECT COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data;

-- Sales by Region
SELECT
    Region,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY Region
ORDER BY Total_Sales DESC;

-- Sales by Product
SELECT
    Product,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY Product
ORDER BY Total_Sales DESC;

-- Average Sales by Region
SELECT
    Region,
    AVG(Sales) AS Average_Sales
FROM sales_data
GROUP BY Region;

-- Top 5 Highest Sales Orders
SELECT *
FROM sales_data
ORDER BY Sales DESC
LIMIT 5;

-- Monthly Sales Trend
SELECT
    strftime('%Y-%m', Date) AS Month,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY Month
ORDER BY Month;

-- Top Performing Region
SELECT
    Region,
    SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Region
ORDER BY Total_Sales DESC
LIMIT 1;
