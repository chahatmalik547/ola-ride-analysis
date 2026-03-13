import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Analytics Pro", layout="wide")

# 2. SMART DATA CONNECTION (SQL with CSV Fallback)
@st.cache_data
def load_base_data():
    try:
        # Try SQL first
        conn = st.connection("mysql", type="sql")
        return conn.query("SELECT * FROM ola_dataset", ttl=600)
    except Exception:
        # If SQL fails (like on the web), load CSV
        df = pd.read_csv("OLA_DataSet.csv")
        # Clean column names just in case there are spaces
        df.columns = df.columns.str.strip()
        return df

# Initialize Data
df = load_base_data()

# 3. Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Operational Dashboard", "SQL Insights Explorer"])

# --- PAGE 1: OPERATIONAL DASHBOARD ---
if page == "Operational Dashboard":
    st.title("🚖 OLA Executive Operations Report")

    # Safety check: Ensure columns exist before filtering
    if "Booking_Status" in df.columns and "Booking_Value" in df.columns:
        
        # Calculate Metrics
        success_df = df[df["Booking_Status"] == "Success"]
        total_rev = success_df["Booking_Value"].sum()
        total_rides = len(df)
        success_rate = (len(success_df) / total_rides) * 100 if total_rides > 0 else 0
        avg_dist = success_df["Ride_Distance"].mean()

        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"₹{total_rev:,.0f}")
        m2.metric("Success Rate", f"{success_rate:.1f}%")
        m3.metric("Avg Distance", f"{avg_dist:.1f} km")

        st.divider()

        # Visuals
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Revenue by Vehicle Type")
            rev_chart = success_df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
            fig = px.bar(rev_chart, x="Vehicle_Type", y="Booking_Value", color="Vehicle_Type")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Booking Status Distribution")
            status_chart = df["Booking_Status"].value_value_counts().reset_index()
            fig_pie = px.pie(status_chart, names="Booking_Status", values="count")
            st.plotly_chart(fig_pie, use_container_width=True)

# --- PAGE 2: SQL INSIGHTS EXPLORER ---
else:
    st.title("🔍 SQL Insight Explorer")
    st.info("On the web, these queries run against the uploaded CSV for portfolio demonstration.")
    
    # Simple query logic for the web version
    query_option = st.selectbox("Select an Insight", [
        "1. Top 5 Customers", 
        "2. Ratings by Vehicle",
        "3. Incomplete Rides Reason"
    ])

    if query_option == "1. Top 5 Customers":
        res = df.groupby("Customer_ID").size().sort_values(ascending=False).head(5)
        st.write(res)
    elif query_option == "2. Ratings by Vehicle":
        res = df.groupby("Vehicle_Type")["Customer_Rating"].mean()
        st.bar_chart(res)
