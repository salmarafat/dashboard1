import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(layout="wide", page_title="🔥 Advanced Sales Dashboard")

st.title("🔥 Sales Intelligence Dashboard")

# ======================
# LOAD DATA
# ======================
df = pd.read_excel("01KP0NEWVZBJNEDPE4XBJ45KHD.xlsx")

# ======================
# FEATURE ENGINEERING
# ======================
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()

df['Revenue_per_Conversion'] = df['Revenue'] / df['Conversions'].replace(0, 1)

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("🎯 Filters")

channel_filter = st.sidebar.multiselect(
    "Channel",
    df['Channel'].unique(),
    default=df['Channel'].unique()
)

customer_filter = st.sidebar.multiselect(
    "Customer Type",
    df['Customer Type'].unique(),
    default=df['Customer Type'].unique()
)

df = df[df['Channel'].isin(channel_filter)]
df = df[df['Customer Type'].isin(customer_filter)]

# ======================
# KPIs (SMART)
# ======================
total_revenue = df['Revenue'].sum()
total_conversions = df['Conversions'].sum()
avg_order = df['Average Order Size'].mean()
conversion_rate = total_conversions / len(df)
roi = df['Revenue'].sum() / (df['Average Order Size'].sum() + 1)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Revenue", f"${total_revenue:,.0f}")
col2.metric("🎯 Conversions", total_conversions)
col3.metric("🧾 Avg Order", f"${avg_order:.2f}")
col4.metric("📈 Conv Rate", f"{conversion_rate*100:.2f}%")
col5.metric("⚡ ROI", f"{roi:.2f}x")

st.divider()

# ======================
# CHANNEL INTELLIGENCE
# ======================
st.subheader("📊 Channel Intelligence")

channel = df.groupby('Channel').agg({
    'Revenue':'sum',
    'Conversions':'sum'
}).reset_index()

channel['Efficiency'] = channel['Revenue'] / (channel['Conversions'] + 1)

fig1 = px.scatter(
    channel,
    x='Conversions',
    y='Revenue',
    size='Efficiency',
    color='Channel',
    title="Channel Performance Map"
)

st.plotly_chart(fig1, use_container_width=True)

# ======================
# SALES REP RANKING
# ======================
st.subheader("🏆 Sales Rep Ranking")

rep = df.groupby('Sales Rep').agg({
    'Revenue':'sum',
    'Conversions':'sum'
}).reset_index()

rep['Score'] = rep['Revenue']*0.7 + rep['Conversions']*0.3

fig2 = px.bar(rep.sort_values('Score', ascending=False),
              x='Sales Rep', y='Score', color='Score')

st.plotly_chart(fig2, use_container_width=True)

# ======================
# CUSTOMER INSIGHTS
# ======================
st.subheader("👥 Customer Behavior")

cust = df['Customer Type'].value_counts().reset_index()
cust.columns = ['Type','Count']

fig3 = px.pie(cust, names='Type', values='Count')
st.plotly_chart(fig3, use_container_width=True)

# ======================
# TIME INTELLIGENCE
# ======================
st.subheader("⏰ Time Performance")

time = df.groupby('Time of Day')['Revenue'].sum().reset_index()

fig4 = px.bar(time, x='Time of Day', y='Revenue', color='Revenue')
st.plotly_chart(fig4, use_container_width=True)

# ======================
# MONTHLY TREND
# ======================
st.subheader("📅 Monthly Trend")

month = df.groupby('Month')['Revenue'].sum().reset_index()

fig5 = px.line(month, x='Month', y='Revenue', markers=True)
st.plotly_chart(fig5, use_container_width=True)

# ======================
# SMART INSIGHTS ENGINE
# ======================
st.subheader("🧠 AI Insights Engine")

best_channel = channel.sort_values('Revenue', ascending=False).iloc[0]['Channel']
worst_channel = channel.sort_values('Revenue').iloc[0]['Channel']

top_rep = rep.sort_values('Score', ascending=False).iloc[0]['Sales Rep']

st.success(f"🚀 Best Channel → {best_channel}")
st.error(f"⚠️ Weak Channel → {worst_channel}")
st.success(f"🏆 Top Sales Rep → {top_rep}")

if conversion_rate < 0.2:
    st.warning("⚠️ Low conversion rate → optimize funnel")

if roi < 1:
    st.error("❌ Losing money → adjust marketing strategy")

if df['Customer Type'].value_counts(normalize=True).get('Returning',0) < 0.4:
    st.info("💡 Improve retention campaigns")

# ======================
# RAW DATA
# ======================
with st.expander("📄 Raw Data"):
    st.dataframe(df)
