import os
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Sales & Customer Insights', page_icon='📊', layout='wide')

BASE = Path(__file__).resolve().parent
DEFAULT_DATA = BASE / 'Sales_Data.csv'
ALT_DATA = BASE / 'Sales_Data(1).csv'

@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    for c in ['Net_Sales','Profit','Gross_Sales','Cost','Unit_Price','Discount','Quantity','Sales_Cycle_Days']:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    return df

def money(v):
    return f'₹{v:,.0f}'

def pct(v):
    return f'{v:.2f}%'

st.title('📊 Sales & Customer Insights Dashboard')
st.caption('Synthetic B2B portfolio project • SQL + Advanced Excel + Power BI concepts implemented in Python')

with st.sidebar:
    st.header('Controls')
    uploaded = st.file_uploader('Upload Sales_Data.csv', type=['csv'])
    if uploaded:
        df = load_data(uploaded)
    elif DEFAULT_DATA.exists():
        df = load_data(str(DEFAULT_DATA))
    elif ALT_DATA.exists():
        df = load_data(str(ALT_DATA))
    else:
        st.error('Sales_Data.csv not found. Put it in the project folder.')
        st.stop()

    years = sorted(df['Year'].dropna().unique().tolist())
    regions = sorted(df['Region'].dropna().unique().tolist())
    cats = sorted(df['Category'].dropna().unique().tolist())
    segments = sorted(df['Customer_Segment'].dropna().unique().tolist())
    reps = sorted(df['Sales_Rep'].dropna().unique().tolist())
    channels = sorted(df['Lead_Channel'].dropna().unique().tolist())

    sel_year = st.multiselect('Year', years, default=years)
    sel_region = st.multiselect('Region', regions, default=regions)
    sel_cat = st.multiselect('Category', cats, default=cats)
    sel_segment = st.multiselect('Customer Segment', segments, default=segments)
    sel_rep = st.multiselect('Sales Rep', reps, default=reps)
    sel_channel = st.multiselect('Lead Channel', channels, default=channels)

    st.divider()
    st.info('The dataset is synthetic portfolio data and should not be presented as confidential company data.')

f = df[
    df['Year'].isin(sel_year) &
    df['Region'].isin(sel_region) &
    df['Category'].isin(sel_cat) &
    df['Customer_Segment'].isin(sel_segment) &
    df['Sales_Rep'].isin(sel_rep) &
    df['Lead_Channel'].isin(sel_channel)
].copy()

won = f[f['Order_Status'].eq('Won')].copy()
total_revenue = won['Net_Sales'].sum()
total_profit = won['Profit'].sum()
won_orders = len(won)
unique_customers = won['Customer_ID'].nunique()
aov = total_revenue / won_orders if won_orders else 0
margin = total_profit / total_revenue if total_revenue else 0
conversion = won_orders / len(f) if len(f) else 0

# ---------- Executive Overview ----------
st.subheader('1. Executive Overview')
k = st.columns(7)
metrics = [
    ('Total Revenue', money(total_revenue)),
    ('Total Profit', money(total_profit)),
    ('Profit Margin', pct(margin*100)),
    ('Won Orders', f'{won_orders:,}'),
    ('Unique Customers', f'{unique_customers:,}'),
    ('Average Order Value', money(aov)),
    ('Conversion Rate', pct(conversion*100)),
]
for col, (label, value) in zip(k, metrics):
    col.metric(label, value)

c1, c2 = st.columns(2)
monthly = (
    won.assign(Month=won['Order_Date'].dt.to_period('M').astype(str))
       .groupby('Month', as_index=False)
       .agg(Revenue=('Net_Sales', 'sum'), Profit=('Profit', 'sum'))
)
with c1:
    fig = px.line(monthly, x='Month', y='Revenue', markers=True, title='Revenue by Month')
    fig.update_layout(xaxis_title='', yaxis_title='Revenue (₹)')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    category = won.groupby('Category', as_index=False)['Net_Sales'].sum().sort_values('Net_Sales', ascending=False)
    fig = px.bar(category, x='Category', y='Net_Sales', title='Revenue by Category', text_auto='.2s')
    fig.update_layout(xaxis_title='', yaxis_title='Revenue (₹)')
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    region = won.groupby('Region', as_index=False)['Net_Sales'].sum().sort_values('Net_Sales', ascending=False)
    fig = px.bar(region, x='Net_Sales', y='Region', orientation='h', title='Revenue by Region', text_auto='.2s')
    fig.update_layout(xaxis_title='Revenue (₹)', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)
with c4:
    lead = f.groupby('Lead_Channel', as_index=False).agg(Leads=('Order_ID','count'), Won=('Order_Status', lambda x: (x=='Won').sum()))
    lead['Conversion Rate'] = lead['Won'] / lead['Leads'] * 100
    fig = px.pie(lead, names='Lead_Channel', values='Leads', hole=.45, title='Leads by Channel')
    st.plotly_chart(fig, use_container_width=True)

top_customers = won.groupby(['Customer_ID','Customer_Name','Customer_Segment'], as_index=False).agg(Revenue=('Net_Sales','sum'), Orders=('Order_ID','count'), Profit=('Profit','sum')).sort_values('Revenue', ascending=False).head(10)
st.markdown('**Top 10 Customers**')
st.dataframe(top_customers, use_container_width=True, hide_index=True)

# ---------- Customer & Market ----------
st.subheader('2. Customer & Market Insights')
c1, c2 = st.columns(2)
segment = won.groupby('Customer_Segment', as_index=False).agg(Revenue=('Net_Sales','sum'), Profit=('Profit','sum'), Customers=('Customer_ID','nunique'))
with c1:
    fig = px.bar(segment.sort_values('Revenue', ascending=False), x='Customer_Segment', y='Revenue', title='Revenue by Customer Segment', text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    customer_type = won.groupby('Customer_Type', as_index=False)['Net_Sales'].sum()
    fig = px.pie(customer_type, names='Customer_Type', values='Net_Sales', hole=.45, title='New vs Existing Customer Revenue')
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    city = won.groupby('City', as_index=False)['Net_Sales'].sum().sort_values('Net_Sales', ascending=False).head(15)
    fig = px.bar(city, x='Net_Sales', y='City', orientation='h', title='Top Cities by Revenue', text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)
with c4:
    region_customers = won.groupby('Region', as_index=False)['Customer_ID'].nunique().rename(columns={'Customer_ID':'Customers'})
    fig = px.bar(region_customers, x='Region', y='Customers', title='Customer Count by Region', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

segment['Revenue per Customer'] = segment['Revenue'] / segment['Customers'].replace(0, pd.NA)
st.dataframe(segment.sort_values('Revenue', ascending=False), use_container_width=True, hide_index=True)

# ---------- Sales Performance ----------
st.subheader('3. Sales Performance')
c1, c2 = st.columns(2)
rep = f.groupby('Sales_Rep', as_index=False).agg(
    Revenue=('Net_Sales', lambda x: x[f.loc[x.index,'Order_Status'].eq('Won')].sum()),
    Profit=('Profit', lambda x: x[f.loc[x.index,'Order_Status'].eq('Won')].sum()),
    Won_Orders=('Order_Status', lambda x: (x=='Won').sum())
).sort_values('Revenue', ascending=False)
with c1:
    fig = px.bar(rep, x='Sales_Rep', y='Revenue', title='Sales Rep Revenue Ranking', text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.bar(rep.sort_values('Profit', ascending=False), x='Sales_Rep', y='Profit', title='Sales Rep Profit Ranking', text_auto='.2s')
    st.plotly_chart(fig, use_container_width=True)

channel_perf = f.groupby('Lead_Channel', as_index=False).agg(
    Leads=('Order_ID','count'),
    Won=('Order_Status', lambda x: (x=='Won').sum()),
    Avg_Sales_Cycle=('Sales_Cycle_Days','mean')
)
channel_perf['Conversion Rate'] = channel_perf['Won'] / channel_perf['Leads'] * 100
c3, c4 = st.columns(2)
with c3:
    fig = px.bar(channel_perf.sort_values('Conversion Rate', ascending=False), x='Lead_Channel', y='Conversion Rate', title='Conversion Rate by Lead Channel', text_auto='.2f')
    fig.update_layout(yaxis_title='Conversion Rate (%)')
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = px.bar(channel_perf.sort_values('Avg_Sales_Cycle'), x='Lead_Channel', y='Avg_Sales_Cycle', title='Average Sales-Cycle Days by Channel', text_auto='.1f')
    st.plotly_chart(fig, use_container_width=True)

status = f['Order_Status'].value_counts().rename_axis('Status').reset_index(name='Count')
fig = px.bar(status, x='Status', y='Count', title='Won vs Lost vs Open Opportunities', text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# ---------- Business recommendations ----------
st.subheader('4. Automated Business Insights')
if not category.empty:
    top_cat = category.iloc[0]
    st.write(f'• **Category focus:** {top_cat["Category"]} is the highest-revenue category in the selected data.')
if not region.empty:
    top_region = region.iloc[0]
    st.write(f'• **Regional strength:** {top_region["Region"]} contributes the highest revenue.')
if not channel_perf.empty:
    best_channel = channel_perf.sort_values('Conversion Rate', ascending=False).iloc[0]
    fastest_channel = channel_perf.sort_values('Avg_Sales_Cycle').iloc[0]
    st.write(f'• **Lead conversion:** {best_channel["Lead_Channel"]} has the highest conversion rate at {best_channel["Conversion Rate"]:.2f}%.')
    st.write(f'• **Sales cycle:** {fastest_channel["Lead_Channel"]} has the shortest average sales cycle at {fastest_channel["Avg_Sales_Cycle"]:.1f} days.')
if not top_customers.empty:
    st.write(f'• **Account management:** prioritize the highest-value customers shown in the Top 10 table for retention and expansion.')
st.write('• **Management principle:** evaluate revenue together with profit margin, conversion, customer value, and sales-cycle duration.')

with st.expander('Dataset preview'):
    st.write(f'{len(f):,} records after filters')
    st.dataframe(f.head(100), use_container_width=True, hide_index=True)

st.caption('Portfolio project. Dataset is synthetic and intended for practice/placement demonstration.')
