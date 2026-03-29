import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Petrol Bunk Dashboard", layout="wide")

st.title("⛽ Petrol Bunk Sales & Demand Stability Dashboard")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("cleaned_petrol_data.csv")

# Convert Date
df['Date'] = pd.to_datetime(df['Date'])

# -----------------------------
# Calculate DSI
# -----------------------------
mean_sales = df['Total_Fuel_Sales'].mean()
std_sales = df['Total_Fuel_Sales'].std()
cv = std_sales / mean_sales
dsi = 1 / (1 + cv)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

station = st.sidebar.multiselect(
    "Select Station",
    options=df['Station_Name'].unique(),
    default=df['Station_Name'].unique()
)

shift = st.sidebar.multiselect(
    "Select Shift",
    options=df['Shift'].unique(),
    default=df['Shift'].unique()
)

day_type = st.sidebar.multiselect(
    "Select Day Type",
    options=df['Day_Type'].unique(),
    default=df['Day_Type'].unique()
)

# Apply filters
filtered_df = df[
    (df['Station_Name'].isin(station)) &
    (df['Shift'].isin(shift)) &
    (df['Day_Type'].isin(day_type))
]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{filtered_df['Total_Revenue (₦)'].sum():,.0f}")
col2.metric("Total Fuel Sales", f"{filtered_df['Total_Fuel_Sales'].sum():,.0f}")
col3.metric("Average Sales", f"{filtered_df['Total_Fuel_Sales'].mean():,.0f}")
col4.metric("Demand Stability Index", f"{dsi:.3f}")

# -----------------------------
# Trend Analysis
# -----------------------------
st.subheader("📈 Fuel Sales Trend Over Time")

trend_data = filtered_df.groupby('Date')['Total_Fuel_Sales'].sum()

fig, ax = plt.subplots(figsize=(6,4))
trend_data.plot(ax=ax)
ax.set_title("Total Fuel Sales Over Time")
st.pyplot(fig)


st.subheader("🏪 Sales Comparison")
station_data = filtered_df.groupby('Station_Name')['Total_Fuel_Sales'].sum()
fuel_cols = ['AGO_Sales (L)', 'PMS_Sales (L)', 'Diesel_Sales (L)']
fuel_data = filtered_df[fuel_cols].sum()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6,4))
    station_data.plot(kind='bar', ax=ax)
    ax.set_title("Sales by Station")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6,4))
    fuel_data.plot(kind='bar', ax=ax)
    ax.set_title("Fuel Contribution")
    st.pyplot(fig)

st.subheader("📊 Distribution & Relationship")

col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(y=filtered_df['Total_Fuel_Sales'], ax=ax)
    ax.set_title("Sales Distribution")
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots(figsize=(6,4))
    sns.scatterplot(
        x=filtered_df['Total_Fuel_Sales'],
        y=filtered_df['Total_Revenue (₦)'],
        ax=ax
    )
    ax.set_title("Sales vs Revenue")
    st.pyplot(fig)

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.subheader("🔥 Correlation Heatmap")

corr = filtered_df.select_dtypes(include=['int64', 'float64']).corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)
st.pyplot(fig)

# -----------------------------
# Insights Section
# -----------------------------
st.subheader("💡 Key Insights")

st.markdown(f"""
- Demand Stability Index (DSI) is **{dsi:.3f}**, indicating **highly stable demand**
- Fuel sales show consistent trends over time
- Minimal variation across stations
- Strong relationship between sales and revenue
""")