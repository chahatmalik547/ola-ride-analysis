import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="OLA Analytics Pro", layout="wide")

# 2. SMART DATA CONNECTION
# Try SQL first (for your laptop), use CSV if it fails (for the web)
@st.cache_data
def get_data(query_name=None):
    try:
        # Try to connect to your MySQL
        conn = st.connection("mysql", type="sql")
        
        if query_name == "kpi":
            return conn.query("SELECT * FROM ola_dataset") # Simplified for example
        elif query_name == "top_customers":
            return conn.query("SELECT Customer_ID, COUNT(*) as total FROM ola_dataset GROUP BY Customer_ID LIMIT 5")
        # Add other query logic here...
        
    except Exception:
        # FALLBACK: If SQL fails, use the CSV file you uploaded to GitHub
        df = pd.read_csv("OLA_DataSet.csv")
        return df

# --- PAGE LOGIC ---
st.title("🚖 OLA Executive Operations Report")

# Get data (this will now work on the web!)
df = get_data()

# Example Metric from the CSV/SQL data
total_rev = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()
st.metric("Total Revenue", f"₹{total_rev:,.0f}")
