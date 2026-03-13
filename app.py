import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Analytics Pro", layout="wide")

# 2. Establish SQL Connection
# This reads credentials from .streamlit/secrets.toml
conn = st.connection("mysql", type="sql")

# 3. Professional Styling
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

# 4. Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/0/0f/Ola_Cabs_logo.svg/1200px-Ola_Cabs_logo.svg.png", width=100)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Operational Dashboard", "SQL Query Runner"])

# --- PAGE 1: OPERATIONAL DASHBOARD ---
if page == "Operational Dashboard":
    st.title("🚖 OLA Executive Operations Report")
    
    # KPI Query - Getting totals for the top row
    kpi_query = """
        SELECT 
            SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END) as total_rev,
            AVG(CASE WHEN Booking_Status = 'Success' THEN Ride_Distance ELSE NULL END) as avg_dist,
            COUNT(*) as total_rides,
            SUM(CASE WHEN Booking_Status = 'Success' THEN 1 ELSE 0 END) as success_rides
        FROM ola_dataset
    """
    kpi_data = conn.query(kpi_query)
    
    # Top Row: KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Revenue", f"₹{kpi_data['total_rev'][0]:,.0f}")
    m2.metric("Success Rate", f"{(kpi_data['success_rides'][0]/kpi_data['total_rides'][0]*100):.1f}%")
    m3.metric("Avg Distance", f"{kpi_data['avg_dist'][0]:.1f} km")
    m4.metric("Total Bookings", f"{kpi_data['total_rides'][0]:,}")

    st.divider()

    # Visuals using your SQL insights
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("💰 Revenue by Vehicle Type")
        # Query #9 + grouping
        rev_query = "SELECT Vehicle_Type, SUM(Booking_Value) as Revenue FROM ola_dataset WHERE Booking_Status = 'Success' GROUP BY Vehicle_Type"
        rev_df = conn.query(rev_query)
        fig_rev = px.bar(rev_df, x="Vehicle_Type", y="Revenue", color="Vehicle_Type", template="plotly_white")
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_right:
        st.subheader("📉 Cancellation Reasons")
        # Query #10 logic
        cancel_query = "SELECT Booking_Status, COUNT(*) as Count FROM ola_dataset GROUP BY Booking_Status"
        cancel_df = conn.query(cancel_query)
        fig_pie = px.pie(cancel_df, names="Booking_Status", values="Count", hole=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- PAGE 2: SQL QUERY RUNNER ---
else:
    st.title("🔍 SQL Insight Explorer")
    st.markdown("Select a specific pre-defined query from your OLA analysis.")

    # Dictionary of all your 10 queries
    queries = {
        "1. Successful Bookings": "SELECT * FROM ola_dataset WHERE Booking_Status = 'Success'",
        "2. Avg Distance per Vehicle": "SELECT Vehicle_Type, AVG(Ride_Distance) as avg_distance FROM ola_dataset GROUP BY Vehicle_Type",
        "3. Customer Cancellations": "SELECT COUNT(*) as Total FROM ola_dataset WHERE Booking_Status = 'Canceled by Customer'",
        "4. Top 5 Customers": "SELECT Customer_ID, COUNT(Booking_ID) as total_rides FROM ola_dataset GROUP BY Customer_ID ORDER BY total_rides DESC LIMIT 5",
        "5. Driver Issues": "SELECT COUNT(*) as Total FROM ola_dataset WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'",
        "6. Prime Sedan Ratings": "SELECT MAX(Driver_Ratings) as Max, MIN(Driver_Ratings) as Min FROM ola_dataset WHERE Vehicle_Type = 'Prime Sedan'",
        "7. UPI Payments": "SELECT * FROM ola_dataset WHERE Payment_Method = 'UPI'",
        "8. Avg Rating per Vehicle": "SELECT Vehicle_Type, AVG(Customer_Rating) as avg_rating FROM ola_dataset GROUP BY Vehicle_Type",
        "9. Total Success Value": "SELECT SUM(Booking_Value) as Total_Revenue FROM ola_dataset WHERE Booking_Status = 'Success'",
        "10. Incomplete Rides Log": "SELECT Booking_ID, Incomplete_Rides_Reason FROM ola_dataset WHERE Incomplete_Rides = 'Yes'"
    }

    selected_query_name = st.selectbox("Select Insight", list(queries.keys()))
    
    if st.button("Run Query"):
        with st.spinner("Fetching from MySQL..."):
            result_df = conn.query(queries[selected_query_name])
            st.success(f"Analysis complete for: {selected_query_name}")
            st.dataframe(result_df, use_container_width=True)
            
            # Simple automatic charting for numeric results
            if len(result_df.columns) == 2 and result_df.dtypes[1] in ['float64', 'int64']:
                st.bar_chart(result_df.set_index(result_df.columns[0]))