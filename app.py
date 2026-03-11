import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Analytics Pro", layout="wide")

# 2. Professional Styling (CSS)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #00c853; }
    .main { background-color: #f0f2f6; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar for Navigation & Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/0/0f/Ola_Cabs_logo.svg/1200px-Ola_Cabs_logo.svg.png", width=100)
st.sidebar.title("Dashboard Filters")
df = pd.read_csv("OLA_DataSet.csv")

v_type = st.sidebar.multiselect("Select Vehicle Type", options=df["Vehicle_Type"].unique(), default=df["Vehicle_Type"].unique())
p_method = st.sidebar.selectbox("Payment Method", options=["All"] + list(df["Payment_Method"].dropna().unique()))

# Filter Logic
filtered_df = df[df["Vehicle_Type"].isin(v_type)]
if p_method != "All":
    filtered_df = filtered_df[filtered_df["Payment_Method"] == p_method]

# 4. Header Section
st.title("🚖 OLA Executive Operations Report")
st.markdown(f"Analysis for **{len(filtered_df):,}** Total Bookings")

# 5. Top Row: KPI Metrics
success_df = filtered_df[filtered_df["Booking_Status"] == "Success"]
total_rev = success_df["Booking_Value"].sum()
avg_dist = success_df["Ride_Distance"].mean()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Revenue", f"₹{total_rev:,.0f}")
m2.metric("Success Rate", f"{(len(success_df)/len(filtered_df)*100):.1f}%")
m3.metric("Avg Distance", f"{avg_dist:.1f} km")
m4.metric("Avg Rating", f"{success_df['Customer_Rating'].mean():.2f} ⭐")

st.divider()

# 6. Charts Section (Addressing your SQL Insights)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("💰 Revenue by Vehicle Category")
    fig_rev = px.bar(success_df, x="Vehicle_Type", y="Booking_Value", color="Vehicle_Type", 
                     template="plotly_white", text_auto='.2s')
    st.plotly_chart(fig_rev, use_container_width=True)

with col_right:
    st.subheader("📉 Cancellation Root Causes")
    # Combining Customer and Driver cancellations for a full view
    fig_pie = px.pie(filtered_df, names="Booking_Status", hole=0.5, 
                     color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_pie, use_container_width=True)

# 7. Bottom Table: Incomplete Rides (SQL Insight #10)
st.subheader("⚠️ Incomplete Rides Log")
incomplete = filtered_df[filtered_df["Incomplete_Rides"] == "Yes"][["Booking_ID", "Incomplete_Rides_Reason", "Vehicle_Type"]]
st.dataframe(incomplete, use_container_width=True)