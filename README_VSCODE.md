# Sales & Customer Insights — VS Code Version

A complete Python/Streamlit implementation of the Sales & Customer Insights portfolio project.

## What it contains
- `app.py` — interactive dashboard
- `Sales_Data.csv` — supplied synthetic 1,500-row dataset
- `sales_customer_insights.sql` — MySQL analysis queries
- `Sales_Customer_Insights.xlsx` — supplied Excel analysis workbook
- `requirements.txt` — Python dependencies
- `run.bat` — Windows one-click-ish runner

## Run in VS Code

### 1. Open the folder
Open this project folder in VS Code.

### 2. Create a virtual environment
Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\Scripts\activate
```

### 3. Install packages
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard
```bash
python -m streamlit run app.py
```

The browser will open the dashboard. If it does not, open the local URL printed in the VS Code terminal.

## Dashboard pages/sections
The app implements the project's three analytical areas:
1. Executive Overview — KPIs, monthly revenue, category/region revenue, lead mix, top customers.
2. Customer & Market Insights — segment, customer type, city and regional analysis.
3. Sales Performance — sales-rep ranking, channel conversion, sales cycle and opportunity status.

It also provides filters for Year, Region, Category, Customer Segment, Sales Rep and Lead Channel.

## Placement explanation
> I built a Sales and Customer Insights Dashboard using Python, SQL, Excel and Power BI concepts. I used a synthetic B2B dataset to analyze revenue, profitability, customer segments, regions, lead channels and sales-team performance. I created KPI calculations such as conversion rate, average order value and profit margin, then built an interactive dashboard to turn the analysis into business recommendations.

## Important
The dataset is synthetic portfolio data. Do not describe it as confidential company data or as real Texzone/company data.
