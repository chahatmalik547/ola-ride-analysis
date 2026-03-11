import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Operations Dashboard", layout="wide")
st.markdown("# **🚖 OLA Ride Operations Analysis**")
st.write("Real-time executive insights into booking patterns and revenue.")

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("OLA_DataSet.csv")
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
vehicle_type = st.sidebar.multiselect("Select Vehicle Type", options=df["Vehicle_Type"].unique(), default=df["Vehicle_Type"].unique())
status = st.sidebar.multiselect("Booking Status", options=df["Booking_Status"].unique(), default="Success")

# Filtered Data
filtered_df = df[(df["Vehicle_Type"].isin(vehicle_type)) & (df["Booking_Status"].isin(status))]

# 4. KPI Metrics (Top Row)
total_revenue = filtered_df[filtered_df["Booking_Status"] == "Success"]["Booking_Value"].sum()
total_rides = len(filtered_df)
avg_rating = filtered_df["Customer_Rating"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Success Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Bookings", f"{total_rides:,}")
col3.metric("Avg Customer Rating", f"{avg_rating:.2f} ⭐")

st.divider()

# 5. Charts (Middle Row)
col4, col5 = st.columns(2)

with col4:
    st.subheader("Revenue by Vehicle Type")
    fig_rev = px.bar(filtered_df, x="Vehicle_Type", y="Booking_Value", color="Vehicle_Type", barmode="group")
    st.plotly_chart(fig_rev, use_container_width=True)

with col5:
    st.subheader("Booking Status Distribution")
    fig_pie = px.pie(df, names="Booking_Status", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

# 6. Deep Dive: Cancellation Analysis
st.subheader("Why are rides being canceled?")
cancel_df = df[df["Booking_Status"].str.contains("Canceled", na=False)]
fig_cancel = px.histogram(cancel_df, x="Vehicle_Type", color="Booking_Status", barmode="group")
st.plotly_chart(fig_cancel, use_container_width=True)