# Sales & Customer Insights Dashboard — Power BI Guide

## Project purpose
Analyze B2B sales, customer behavior, lead channels, regions, categories and sales-team performance to identify revenue-growth opportunities.

**Important:** The supplied dataset is synthetic and created for portfolio/placement practice. Do not present it as company-confidential or real business data.

## Files
- `Sales_Data.csv` — Power BI import file
- `Sales_Customer_Insights.xlsx` — Excel analysis workbook
- `sales_customer_insights.sql` — MySQL analysis queries
- `README.md` — project explanation

## Recommended Power BI pages

### Page 1 — Executive Overview
KPI cards:
- Total Revenue
- Total Profit
- Profit Margin
- Won Orders
- Unique Customers
- Average Order Value
- Conversion Rate

Visuals:
1. Line chart: Revenue by Month
2. Column chart: Revenue by Category
3. Bar chart: Revenue by Region
4. Donut chart: Leads by Channel
5. Table: Top 10 Customers

Slicers:
- Year
- Quarter
- Region
- Category
- Customer Segment
- Sales Rep
- Lead Channel

### Page 2 — Customer & Market Insights
Visuals:
- Revenue by Customer Segment
- New vs Existing Customer Revenue
- Top 10 Customers
- Revenue by City
- Customer count by region
- Average order value by segment

Business questions:
- Which customer segments generate the most revenue?
- Which cities/regions have expansion potential?
- Which customers should receive priority account management?

### Page 3 — Sales Performance
Visuals:
- Sales Rep revenue ranking
- Sales Rep profit ranking
- Conversion rate by lead channel
- Average sales-cycle days by channel
- Won vs Lost vs Open opportunities

Business questions:
- Which channels convert best?
- Which sales reps contribute most revenue?
- Where can the sales process be improved?

## Suggested DAX measures

```DAX
Total Revenue =
CALCULATE(
    SUM(Sales_Data[Net_Sales]),
    Sales_Data[Order_Status] = "Won"
)

Total Profit =
CALCULATE(
    SUM(Sales_Data[Profit]),
    Sales_Data[Order_Status] = "Won"
)

Profit Margin =
DIVIDE([Total Profit], [Total Revenue])

Won Orders =
CALCULATE(
    COUNTROWS(Sales_Data),
    Sales_Data[Order_Status] = "Won"
)

Unique Customers =
CALCULATE(
    DISTINCTCOUNT(Sales_Data[Customer_ID]),
    Sales_Data[Order_Status] = "Won"
)

Average Order Value =
DIVIDE([Total Revenue], [Won Orders])

Conversion Rate =
DIVIDE(
    CALCULATE(COUNTROWS(Sales_Data), Sales_Data[Order_Status]="Won"),
    COUNTROWS(Sales_Data)
)
```

## Recommended data model
For a portfolio version, a single fact table is sufficient. If you want a stronger Power BI model, create:
- FactSales
- DimCustomer
- DimDate
- DimProduct
- DimSalesRep
- DimChannel
- DimGeography

Connect each dimension to FactSales using the relevant key.

## Dashboard storytelling
Start with:
1. How much revenue and profit are being generated?
2. Which products/categories drive revenue?
3. Which regions and customer segments are strongest?
4. Which acquisition channels convert?
5. Which customers and sales reps deserve attention?
6. What business actions should management take?
