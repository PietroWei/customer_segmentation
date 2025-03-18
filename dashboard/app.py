import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect("dbname=yourdb user=youruser password=yourpass host=localhost")

# Extract RFM data
df_rfm = pd.read_sql_query("""
    SELECT customer_id, 
           EXTRACT(DAY FROM (NOW() - MAX(sale_date))) AS recency,
           COUNT(DISTINCT invoice_no) AS frequency,
           SUM(total_amount) AS monetary
    FROM sales 
    GROUP BY customer_id;
""", conn)

# Normalize RFM values
rfm_values = df_rfm[['recency', 'frequency', 'monetary']]
rfm_values = (rfm_values - rfm_values.mean()) / rfm_values.std()

# Perform K-Means clustering
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
df_rfm['cluster'] = kmeans.fit_predict(rfm_values)

# Close database connection
conn.close()

# Create Streamlit dashboard
st.title("Customer Segmentation & Retention Analysis")
st.write("This dashboard shows customer segments using the RFM model.")
fig = px.scatter_3d(df_rfm, x='recency', y='frequency', z='monetary', color='cluster', title="Customer Segments")
st.plotly_chart(fig)