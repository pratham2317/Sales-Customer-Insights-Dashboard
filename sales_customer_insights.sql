-- SALES & CUSTOMER INSIGHTS PROJECT
-- Synthetic B2B dataset for portfolio/placement use.
-- Database: MySQL 8+
-- Import Sales_Data.csv into a table named sales_data before running.

CREATE DATABASE IF NOT EXISTS sales_analytics;
USE sales_analytics;

-- Expected table columns:
-- Order_ID, Order_Date, Customer_ID, Customer_Name, Customer_Segment, City, Region,
-- Category, Product, Lead_Channel, Sales_Rep, Order_Status, Quantity, Unit_Price,
-- Discount, Gross_Sales, Net_Sales, Cost, Profit, Month, Quarter, Year,
-- Lead_ID, Lead_Status, Sales_Cycle_Days, Customer_Type

-- 1. Overall KPIs
SELECT
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS total_revenue,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Profit ELSE 0 END),2) AS total_profit,
    COUNT(CASE WHEN Order_Status='Won' THEN 1 END) AS won_orders,
    COUNT(DISTINCT CASE WHEN Order_Status='Won' THEN Customer_ID END) AS unique_customers,
    ROUND(
        SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END) /
        NULLIF(COUNT(CASE WHEN Order_Status='Won' THEN 1 END),0),2
    ) AS average_order_value,
    ROUND(
        SUM(CASE WHEN Order_Status='Won' THEN 1 ELSE 0 END) / COUNT(*) * 100,2
    ) AS conversion_rate_pct
FROM sales_data;

-- 2. Monthly revenue and profit
SELECT
    DATE_FORMAT(Order_Date,'%Y-%m') AS month,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Profit ELSE 0 END),2) AS profit,
    COUNT(CASE WHEN Order_Status='Won' THEN 1 END) AS won_orders
FROM sales_data
GROUP BY DATE_FORMAT(Order_Date,'%Y-%m')
ORDER BY month;

-- 3. Category performance
SELECT
    Category,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Profit ELSE 0 END),2) AS profit,
    COUNT(CASE WHEN Order_Status='Won' THEN 1 END) AS orders
FROM sales_data
GROUP BY Category
ORDER BY revenue DESC;

-- 4. Regional performance
SELECT
    Region,
    COUNT(DISTINCT CASE WHEN Order_Status='Won' THEN Customer_ID END) AS customers,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Profit ELSE 0 END),2) AS profit
FROM sales_data
GROUP BY Region
ORDER BY revenue DESC;

-- 5. Lead-channel conversion
SELECT
    Lead_Channel,
    COUNT(*) AS leads,
    SUM(CASE WHEN Order_Status='Won' THEN 1 ELSE 0 END) AS won,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS conversion_rate_pct,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue
FROM sales_data
GROUP BY Lead_Channel
ORDER BY conversion_rate_pct DESC;

-- 6. Sales representative performance
SELECT
    Sales_Rep,
    COUNT(CASE WHEN Order_Status='Won' THEN 1 END) AS won_orders,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Profit ELSE 0 END),2) AS profit
FROM sales_data
GROUP BY Sales_Rep
ORDER BY revenue DESC;

-- 7. Top 10 customers
SELECT
    Customer_ID,
    Customer_Name,
    Customer_Segment,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue,
    COUNT(CASE WHEN Order_Status='Won' THEN 1 END) AS orders
FROM sales_data
GROUP BY Customer_ID, Customer_Name, Customer_Segment
ORDER BY revenue DESC
LIMIT 10;

-- 8. New vs existing customer revenue
SELECT
    Customer_Type,
    COUNT(DISTINCT Customer_ID) AS customers,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue
FROM sales_data
GROUP BY Customer_Type;

-- 9. Average sales cycle by channel
SELECT
    Lead_Channel,
    ROUND(AVG(Sales_Cycle_Days),1) AS avg_sales_cycle_days
FROM sales_data
GROUP BY Lead_Channel
ORDER BY avg_sales_cycle_days;

-- 10. High-value customer opportunities
SELECT
    Customer_ID,
    Customer_Name,
    Customer_Segment,
    ROUND(SUM(CASE WHEN Order_Status='Won' THEN Net_Sales ELSE 0 END),2) AS revenue,
    COUNT(CASE WHEN Order_Status='Won' THEN 1 END) AS orders
FROM sales_data
GROUP BY Customer_ID, Customer_Name, Customer_Segment
HAVING revenue > 300000
ORDER BY revenue DESC;