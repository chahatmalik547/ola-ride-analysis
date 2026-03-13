import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Analytics Pro", layout="wide", page_icon="🚖")

# 2. SMART DATA CONNECTION (SQL with CSV Fallback)
# We use @st.cache_data so the app stays fast and doesn't spam the DB
@st.cache_data(ttl=600)
def load_data():
    try:
        # Try to connect to Local MySQL (Works on your laptop)
        # Ensure your .streamlit/secrets.toml has dialect = "mysql+pymysql"
        conn = st.connection("mysql", type="sql")
        df = conn.query("SELECT * FROM ola_dataset")
        return df, "Live SQL Database"
    except Exception as e:
        # FALLBACK: Load CSV (Works on Streamlit Cloud/Web)
        try:
            df = pd.read_csv("OLA_DataSet.csv")
            # Cleaning: remove spaces from headers and handle dates
            df.columns = df.columns.str.strip()
            return df, "Static CSV File"
        except Exception:
            return pd.DataFrame(), "No Data Found"

# Initialize Data and Source Label
df, data_source = load_data()

# 3. Sidebar Styling & Navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/0/0f/Ola_Cabs_logo.svg/1200px-Ola_Cabs_logo.svg.png", width=100)
st.sidebar.title("OLA Dashboard")

# --- DATA SOURCE INDICATOR ---
# This answers your question: "How to check if it's SQL or CSV"
if data_source == "Live SQL Database":
    st.sidebar.success(f"📁 Source: {data_source}")
else:
    st.sidebar.warning(f"📁 Source: {data_source}")

page = st.sidebar.radio("Navigate View", ["Operational Dashboard", "SQL Insights Explorer"])

# Main Application Logic
if not df.empty:
    
    # --- PAGE 1: OPERATIONAL DASHBOARD ---
    if page == "Operational Dashboard":
        st.title("🚖 OLA Executive Operations Report")
        st.markdown(f"Currently analyzing **{len(df):,}** ride records.")

        # Metric Calculations
        success_df = df[df["Booking_Status"] == "Success"]
        total_rev = success_df["Booking_Value"].sum()
        total_rides = len(df)
        success_rate = (len(success_df) / total_rides * 100) if total_rides > 0 else 0
        avg_dist = success_df["Ride_Distance"].mean()

        # Top Row Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"₹{total_rev:,.0f}")
        m2.metric("Success Rate", f"{success_rate:.1f}%")
        m3.metric("Avg Distance", f"{avg_dist:.1f} km")

        st.divider()

        # Charts Row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Revenue by Vehicle Type")
            rev_chart = success_df.groupby("Vehicle_Type")["Booking_Value"].sum().reset_index()
            fig_bar = px.bar(rev_chart, x="Vehicle_Type", y="Booking_Value", 
                             color="Vehicle_Type", text_auto='.2s',
                             template="plotly_white")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("📉 Booking Status Breakdown")
            # Fixed the typo here from previous version
            status_chart = df["Booking_Status"].value_counts().reset_index()
            fig_pie = px.pie(status_chart, names="Booking_Status", values="count", hole=0.5)
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- PAGE 2: SQL INSIGHTS EXPLORER ---
    else:
        st.title("🔍 SQL Insight Explorer")
        st.write("Below are the pre-defined queries for the OLA Ride Analysis project.")

        query_option = st.selectbox("Select Business Query", [
            "1. Successful Bookings",
            "2. Average Distance per Vehicle",
            "3. Top 5 Customers by Volume",
            "4. Ratings Analysis",
            "5. Incomplete Rides Breakdown"
        ])

        # Logic for the 10 core insights
        if query_option == "1. Successful Bookings":
            st.dataframe(df[df["Booking_Status"] == "Success"].head(50))
            
        elif query_option == "2. Average Distance per Vehicle":
            res = df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index()
            fig = px.line(res, x="Vehicle_Type", y="Ride_Distance", markers=True)
            st.plotly_chart(fig)

        elif query_option == "3. Top 5 Customers by Volume":
            res = df["Customer_ID"].value_counts().head(5).reset_index()
            res.columns = ["Customer ID", "Ride Count"]
            st.table(res)

        elif query_option == "4. Ratings Analysis":
            res = df.groupby("Vehicle_Type")["Customer_Rating"].mean().sort_values(ascending=False)
            st.bar_chart(res)
            
        elif query_option == "5. Incomplete Rides Breakdown":
            incomplete = df[df["Incomplete_Rides"] == "Yes"]
            if not incomplete.empty:
                res = incomplete["Incomplete_Rides_Reason"].value_counts().reset_index()
                st.write(res)
            else:
                st.info("No incomplete rides found in current dataset.")

else:
    st.error("Unable to load data. Please ensure OLA_DataSet.csv is in the root folder or MySQL is connected.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Data Analyst Portfolio Project")
