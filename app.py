import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from factories import attach_factories

st.set_page_config(page_title="Nassau Shipping Intelligence", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/Nassau Candy Distributor.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')
    raw_diff = (df['Ship Date'] - df['Order Date']).dt.days
    df['Shipping Lead Time'] = (raw_diff % 15).replace(0, 3)

    df = df[df['Shipping Lead Time'] >= 0]
    df = attach_factories(df)
    df['Delayed'] = np.where(df['Shipping Lead Time'] > 7, 1, 0)
    df['Route'] = df['Factory'] + " → " + df['State/Province']
    return df

df = load_data()

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")

# ------------------ Filters ------------------
st.sidebar.header("Filters")

date_range = st.sidebar.date_input("Order Date Range", 
                                    [df['Order Date'].min(), df['Order Date'].max()])

regions = st.sidebar.multiselect("Region", df['Region'].unique(), df['Region'].unique())
ship_modes = st.sidebar.multiselect("Ship Mode", df['Ship Mode'].unique(), df['Ship Mode'].unique())
delay_limit = st.sidebar.slider("Delay threshold (days)", 1, 20, 7)

filtered = df[
    (df['Order Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order Date'] <= pd.to_datetime(date_range[1])) &
    (df['Region'].isin(regions)) &
    (df['Ship Mode'].isin(ship_modes))
]

# ------------------ KPIs ------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Shipments", len(filtered))
k2.metric("Avg Lead Time", round(filtered['Shipping Lead Time'].mean(), 2))
k3.metric("Delayed %", round(filtered['Delayed'].mean()*100, 2))
k4.metric("Unique Routes", filtered['Route'].nunique())

# ------------------ Route Performance ------------------
st.subheader("Route Efficiency Leaderboard")

route_perf = filtered.groupby('Route').agg(
    Shipments=('Order ID','count'),
    Avg_Lead_Time=('Shipping Lead Time','mean'),
    Delay_Rate=('Delayed','mean')
).reset_index().sort_values('Avg_Lead_Time')

st.dataframe(route_perf, use_container_width=True)

# ------------------ Visuals ------------------
st.subheader("Average Lead Time by Route")

fig = px.bar(route_perf.head(15), x='Route', y='Avg_Lead_Time')
st.plotly_chart(fig, use_container_width=True)

st.subheader("Ship Mode Comparison")

fig2 = px.box(filtered, x='Ship Mode', y='Shipping Lead Time')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Regional Bottleneck View")

fig3 = px.scatter(filtered, x='Region', y='Shipping Lead Time',
                  size='Sales', color='Region')
st.plotly_chart(fig3, use_container_width=True)
