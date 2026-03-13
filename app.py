import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Analytics Pro", layout="wide")

# 2. SMART DATA CONNECTION (SQL with CSV Fallback)
@st.cache_data
def load_data():
    try:
        # Try to connect to your Local MySQL (Works on your laptop)
        conn = st.connection("mysql", type="sql")
        df = conn.query("SELECT * FROM ola_dataset", ttl=600)
        return df
    except Exception:
        # FALLBACK: Load CSV (Works on Streamlit Cloud/Web)
        try:
            df = pd.read_csv("OLA_DataSet.csv")
            df.columns = df.columns.str.strip() # Clean column names
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()

# Initialize Data
df = load_data()

# 3. Sidebar Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/0/0f/Ola_Cabs_logo.svg/1200px-Ola_Cabs_logo.svg.png", width=100)
st.sidebar.title("OLA Analytics")
page = st.sidebar.radio("Navigate", ["Operational Dashboard", "SQL Insights Explorer"])

if not df.empty:
    # --- PAGE 1: OPERATIONAL DASHBOARD ---
    if page == "Operational Dashboard":
        st.title("🚖 OLA Executive Operations Report")

        # Top Level Metrics
        success_df = df[df["Booking_Status"] == "Success"]
        total_rev = success_df["Booking_Value"].sum()
        total_rides = len(df)
        success_rate = (len(success_df) / total_rides * 100) if total_rides > 0 else 0
        avg_dist = success_df["Ride_Distance"].mean()

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"₹{total_rev:,.0f}")
        m2.metric("Success Rate", f"{success_rate:.1f}%")
        m3.metric("Avg Distance", f"{avg_dist:.1f} km")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("💰 Revenue by Vehicle Type")
            rev_chart = success_df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
            fig_bar = px.bar(rev_chart, x="Vehicle_Type", y="Booking_Value", 
                             color="Vehicle_Type", template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("📉 Booking Status Breakdown")
            # FIXED: Changed value_value_counts to value_counts
            status_chart = df["Booking_Status"].value_counts().reset_index()
            fig_pie = px.pie(status_chart, names="Booking_Status", values="count", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- PAGE 2: SQL INSIGHTS EXPLORER ---
    else:
        st.title("🔍 SQL Insight Explorer")
        st.markdown("Detailed breakdown of the 10 core business queries.")

        query_option = st.selectbox("Select an Insight to View", [
            "1. Successful Bookings",
            "2. Avg Distance per Vehicle",
            "3. Top 5 Customers by Volume",
            "4. Ratings Analysis",
            "5. Incomplete Rides Breakdown"
        ])

        if query_option == "1. Successful Bookings":
            res = df[df["Booking_Status"] == "Success"]
            st.dataframe(res.head(100))
            
        elif query_option == "2. Avg Distance per Vehicle":
            res = df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index()
            st.bar_chart(res.set_index("Vehicle_Type"))

        elif query_option == "3. Top 5 Customers by Volume":
            res = df["Customer_ID"].value_counts().head(5).reset_index()
            st.table(res)

        elif query_option == "4. Ratings Analysis":
            res = df.groupby("Vehicle_Type")["Customer_Rating"].mean().reset_index()
            st.line_chart(res.set_index("Vehicle_Type"))
            
        elif query_option == "5. Incomplete Rides Breakdown":
            incomplete = df[df["Incomplete_Rides"] == "Yes"]
            res = incomplete["Incomplete_Rides_Reason"].value_counts().reset_index()
            st.dataframe(res)

else:
    st.warning("⚠️ Data could not be loaded. Please check your SQL connection or CSV file path.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by Chahat Malik")
