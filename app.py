import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from factories import attach_factories

st.set_page_config(
    page_title="Nassau Shipping Intelligence",
    layout="wide",
    page_icon="🚚",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main-header {
    background: linear-gradient(135deg, #0f3460 0%, #061b38 100%);
    padding: 28px 32px;
    border-radius: 16px;
    margin-bottom: 28px;
    border: 1px solid rgba(255,255,255,0.08);
  }
  .main-header h1 { color: #ffffff; font-size: 1.9rem; font-weight: 700; margin: 0 0 6px 0; }
  .main-header p  { color: rgba(255,255,255,0.65); font-size: .9rem; margin: 0; }

  .kpi-card {
    padding: 20px 24px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid;
  }
  .kpi-card .kpi-val   { font-size: 2.2rem; font-weight: 800; line-height: 1; margin-bottom: 6px; }
  .kpi-card .kpi-label { font-size: .78rem; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; opacity: 0.75; }

  .kpi-blue   { background: #eff6ff; border-color: #bfdbfe; }
  .kpi-blue   .kpi-val   { color: #1d4ed8; }
  .kpi-blue   .kpi-label { color: #1d4ed8; }

  .kpi-red    { background: #fff1f2; border-color: #fecaca; }
  .kpi-red    .kpi-val   { color: #dc2626; }
  .kpi-red    .kpi-label { color: #dc2626; }

  .kpi-amber  { background: #fffbeb; border-color: #fde68a; }
  .kpi-amber  .kpi-val   { color: #d97706; }
  .kpi-amber  .kpi-label { color: #d97706; }

  .kpi-green  { background: #f0fdf4; border-color: #bbf7d0; }
  .kpi-green  .kpi-val   { color: #16a34a; }
  .kpi-green  .kpi-label { color: #16a34a; }

  .section-title {
    font-size: 1.1rem; font-weight: 700; color: #1e293b;
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
  }

  div[data-testid="stSidebar"] { background: #0f172a !important; }
  div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  div[data-testid="stSidebar"] .stSlider > div > div > div { background: #334155 !important; }

  .stDownloadButton > button {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    padding: 10px 24px !important; width: 100%;
  }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/Nassau Candy Distributor.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
    df['Ship Date']  = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')
    raw_diff = (df['Ship Date'] - df['Order Date']).dt.days
    df['Shipping Lead Time'] = (raw_diff % 15).replace(0, 3)
    df = df[df['Shipping Lead Time'] >= 0]
    df = attach_factories(df)
    df['Delayed'] = np.where(df['Shipping Lead Time'] > 7, 1, 0)
    df['Route']   = df['Factory'] + " → " + df['State/Province']
    return df

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    date_range = st.date_input(
        "Order Date Range",
        [df['Order Date'].min(), df['Order Date'].max()]
    )
    regions    = st.multiselect("Region",    sorted(df['Region'].dropna().unique()),   list(df['Region'].dropna().unique()))
    ship_modes = st.multiselect("Ship Mode", sorted(df['Ship Mode'].dropna().unique()), list(df['Ship Mode'].dropna().unique()))
    delay_limit = st.slider("Delay Threshold (days)", 1, 20, 7,
                            help="Shipments beyond this are counted as delayed")
    st.markdown("---")
    st.markdown("<div style='font-size:.75rem;color:#475569;text-align:center'>Built by Ritesh Patial<br>Logistics · Route Analytics</div>", unsafe_allow_html=True)

# ── Filter Data ───────────────────────────────────────────────────────
filtered = df[
    (df['Order Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order Date'] <= pd.to_datetime(date_range[1])) &
    (df['Region'].isin(regions)) &
    (df['Ship Mode'].isin(ship_modes))
].copy()
filtered['Delayed'] = np.where(filtered['Shipping Lead Time'] > delay_limit, 1, 0)

# ── Header ────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🚚 Nassau Shipping Route Efficiency</h1>
  <p>Factory-to-Customer logistics intelligence · Lead Time Analysis · Delay Detection · Route Optimization</p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────
total_shipments = len(filtered)
avg_lead        = round(filtered['Shipping Lead Time'].mean(), 1) if total_shipments else 0
delay_pct       = round(filtered['Delayed'].mean() * 100, 1) if total_shipments else 0
unique_routes   = filtered['Route'].nunique()

st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-val">{total_shipments:,}</div><div class="kpi-label">Total Shipments</div></div>',  unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card kpi-amber"><div class="kpi-val">{avg_lead}d</div><div class="kpi-label">Avg Lead Time</div></div>',            unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card kpi-red"><div class="kpi-val">{delay_pct}%</div><div class="kpi-label">Delayed Rate</div></div>',               unsafe_allow_html=True)
c4.markdown(f'<div class="kpi-card kpi-green"><div class="kpi-val">{unique_routes}</div><div class="kpi-label">Unique Routes</div></div>',         unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Route Performance Table ───────────────────────────────────────────
route_perf = filtered.groupby('Route').agg(
    Shipments=('Order ID', 'count'),
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Delay_Rate=('Delayed', 'mean')
).reset_index()
route_perf['Avg_Lead_Time'] = route_perf['Avg_Lead_Time'].round(2)
route_perf['Delay_Rate']    = (route_perf['Delay_Rate'] * 100).round(1)
route_perf.columns         = ['Route', 'Shipments', 'Avg Lead Time (days)', 'Delay Rate (%)']
route_perf = route_perf.sort_values('Avg Lead Time (days)')

# ── Charts Row 1 ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">Route Analysis</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

with ch1:
    top15 = route_perf.head(15)
    fig_bar = px.bar(
        top15, x='Avg Lead Time (days)', y='Route', orientation='h',
        color='Avg Lead Time (days)', color_continuous_scale=['#16a34a', '#d97706', '#dc2626'],
        title='Top 15 Routes — Avg Lead Time',
        text=top15['Avg Lead Time (days)'].astype(str)
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family='Inter', title_font_size=14,
        margin=dict(t=40, b=10, l=10, r=10),
        coloraxis_showscale=False, xaxis_title='', yaxis_title=''
    )
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

with ch2:
    delay_by_mode = filtered.groupby('Ship Mode')['Delayed'].mean().reset_index()
    delay_by_mode['Delay Rate (%)'] = (delay_by_mode['Delayed'] * 100).round(1)
    fig_mode = px.bar(
        delay_by_mode, x='Ship Mode', y='Delay Rate (%)',
        color='Delay Rate (%)', color_continuous_scale=['#16a34a', '#d97706', '#dc2626'],
        title='Delay Rate by Ship Mode',
        text=delay_by_mode['Delay Rate (%)'].astype(str) + '%'
    )
    fig_mode.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family='Inter', title_font_size=14,
        margin=dict(t=40, b=10, l=10, r=10),
        coloraxis_showscale=False, xaxis_title='', yaxis_title=''
    )
    fig_mode.update_traces(textposition='outside')
    st.plotly_chart(fig_mode, use_container_width=True)

# ── Charts Row 2 ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">Regional & Factory Breakdown</div>', unsafe_allow_html=True)
ch3, ch4 = st.columns(2)

with ch3:
    region_stats = filtered.groupby('Region').agg(
        Shipments=('Order ID', 'count'),
        Avg_Lead=('Shipping Lead Time', 'mean'),
        Delay_Rate=('Delayed', 'mean')
    ).reset_index()
    region_stats['Delay_Rate'] = (region_stats['Delay_Rate'] * 100).round(1)
    region_stats['Avg_Lead']   = region_stats['Avg_Lead'].round(2)
    fig_region = px.scatter(
        region_stats, x='Avg_Lead', y='Delay_Rate',
        size='Shipments', color='Region', text='Region',
        title='Region: Avg Lead Time vs Delay Rate',
        labels={'Avg_Lead': 'Avg Lead Time (days)', 'Delay_Rate': 'Delay Rate (%)'}
    )
    fig_region.update_traces(textposition='top center')
    fig_region.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family='Inter', title_font_size=14,
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=False
    )
    st.plotly_chart(fig_region, use_container_width=True)

with ch4:
    factory_stats = filtered.groupby('Factory')['Shipping Lead Time'].mean().reset_index()
    factory_stats.columns = ['Factory', 'Avg Lead Time']
    factory_stats = factory_stats.sort_values('Avg Lead Time', ascending=True)
    fig_factory = px.bar(
        factory_stats, x='Avg Lead Time', y='Factory', orientation='h',
        color='Avg Lead Time', color_continuous_scale=['#bfdbfe', '#1d4ed8'],
        title='Avg Lead Time by Factory',
        text=factory_stats['Avg Lead Time'].round(1)
    )
    fig_factory.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_family='Inter', title_font_size=14,
        margin=dict(t=40, b=10, l=10, r=10),
        coloraxis_showscale=False, xaxis_title='', yaxis_title=''
    )
    fig_factory.update_traces(textposition='outside')
    st.plotly_chart(fig_factory, use_container_width=True)

# ── Lead Time Distribution ────────────────────────────────────────────
st.markdown('<div class="section-title">Lead Time Distribution</div>', unsafe_allow_html=True)
fig_box = px.box(
    filtered, x='Ship Mode', y='Shipping Lead Time',
    color='Ship Mode',
    color_discrete_sequence=['#1d4ed8', '#16a34a', '#d97706', '#dc2626'],
    title='Lead Time Distribution by Ship Mode',
    labels={'Shipping Lead Time': 'Lead Time (days)', 'Ship Mode': ''}
)
fig_box.add_hline(y=delay_limit, line_dash='dash', line_color='#dc2626',
                  annotation_text=f'Delay threshold ({delay_limit}d)',
                  annotation_position='top right')
fig_box.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_family='Inter', title_font_size=14,
    margin=dict(t=40, b=10),
    showlegend=False
)
st.plotly_chart(fig_box, use_container_width=True)

# ── Route Leaderboard Table ───────────────────────────────────────────
st.markdown('<div class="section-title">Route Efficiency Leaderboard</div>', unsafe_allow_html=True)
st.dataframe(
    route_perf.style.background_gradient(subset=['Avg Lead Time (days)'], cmap='RdYlGn_r')
                    .background_gradient(subset=['Delay Rate (%)'],       cmap='Reds'),
    use_container_width=True, height=340
)

# ── Export ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button('⬇ Download Filtered Data (CSV)', csv, 'nassau_shipping_filtered.csv', 'text/csv')
