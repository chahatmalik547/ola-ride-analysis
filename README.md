🚖 OLA Ride Operations: End-to-End Analysis Dashboard
This project delivers a deep-dive analysis into OLA’s ride-booking operations. By processing over 100,000 records, I have transformed raw data into strategic business insights using SQL for data engineering, Power BI for visualization, and Streamlit for interactive deployment.

📂 Project Overview
The objective of this project is to optimize ride-hailing performance. By analyzing booking success rates, cancellation patterns, and revenue flow, I have created a roadmap to improve platform reliability and customer satisfaction.

🛠️ The Power Trio (Tech Stack)
SQL: The engine used for cleaning raw data and extracting complex KPIs.

Power BI: The storytelling tool used to build interactive executive dashboards.

Streamlit: The deployment platform that turns the analysis into a live web application.

💡 Business Insights & Strategic Objectives
1. Platform Reliability & Performance
By isolating all Success bookings, I measured the system's efficiency in matching riders with drivers. This metric serves as the primary heartbeat of the OLA platform’s health.

2. Fleet & Fuel Maintenance
I calculated the Average Ride Distance across all vehicle types (Auto, Bike, Prime Sedan, etc.). This data helps in predictive maintenance and fuel budgeting for different vehicle segments.

3. Root Cause Cancellation Analysis
I performed a dual-sided analysis of why rides fail:

Customer Friction: High cancellation rates highlight issues with wait times or pricing.

Driver Support: Identifying cancellations due to "Personal & Car related issues" helps flag where drivers need better technical support.

4. VIP Customer Retention
Using SQL aggregation, I identified the Top 5 Customers with the highest booking frequency. This allows for targeted loyalty rewards and high-value marketing.

5. Premium Service Monitoring
For the Prime Sedan category, I monitored the spread between maximum and minimum ratings. This ensures that the "Premium" experience remains consistent for high-paying users.

6. Digital Adoption Tracking
By analyzing payments made via UPI, I tracked the transition toward a cashless ecosystem, which significantly reduces cash-handling risks and operational overhead.

7. Revenue & Leakage Tracking
I calculated the Total Booking Value of successful trips to define the bottom line. Simultaneously, I analyzed Incomplete Rides to understand exactly where and why the business is losing potential revenue.

🖼️ Visual Insights
Power BI Executive Dashboard
The dashboard provides a high-level view of operations, featuring real-time KPI cards, revenue trends, and rating distributions.

(Example visualization representing the distribution of revenue across vehicle types)

Streamlit Interactive Interface
The Streamlit app allows stakeholders to interactively filter data by vehicle type, payment method, or date to see the report's insights in real-time.

🚀 Project Workflow
Analyze: Running the 10 core SQL queries found in the Executive Report.

Visualize: Building dynamic DAX measures and visuals in Power BI.

Deploy: Packaging the insights into a clean, accessible Streamlit web interface.
